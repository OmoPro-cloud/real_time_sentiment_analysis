import csv
import json
import re
import time
from pathlib import Path
from typing import Dict, Optional, List, Tuple

import requests
from bs4 import BeautifulSoup

# Bible book abbreviations and chapter counts
BOOKS = {
    "GEN": 50,
    "EXO": 40,
    "LEV": 27,
    "NUM": 36,
    "DEU": 34,
    "JOS": 24,
    "JDG": 21,
    "RUT": 4,
    "1SA": 31,
    "2SA": 24,
}

OUTPUT_FILE = "para_pairs.csv"
TARGET_PAIRS = 1000
BASE_URL_TEMPLATE = "https://www.bible.com/bible/2616/{BOOK}.{CHAPTER}.UBV77?parallel=114"


def fetch_chapter_html(book: str, chapter: int, timeout: int = 10) -> Optional[str]:
    """Fetch HTML for a specific chapter."""
    url = BASE_URL_TEMPLATE.format(BOOK=book, CHAPTER=chapter)
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to fetch {book} {chapter}: {e}")
        return None


def extract_next_data(html: str) -> Optional[dict]:
    """Extract __NEXT_DATA__ JSON from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    # Preferred: explicit script tag with id
    tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
    if not tag:
        return None
    try:
        return json.loads(tag.string)
    except Exception: None

    # Fallback: search any script that contains __NEXT_DATA__ or a JSON with pageProps
    for script in soup.find_all("script"):
        txt = script.string or script.get_text() or ""
        if "__NEXT_DATA__" in txt or '"pageProps"' in txt:
            # try to extract an assignment like: window.__NEXT_DATA__ = {...};
            m = re.search(r"__NEXT_DATA__\s*=\s*({.*});", txt, flags=re.S)
            if not m:
                # try to find a JSON object containing pageProps
                m = re.search(r"(\{\s*\"props\".*\})", txt, flags=re.S)
            if m:
                try:
                    return json.loads(m.group(1))
                except Exception:
                    # last resort: try to load the whole script text as JSON
                    try:
                        return json.loads(txt.strip())
                    except Exception:
                        continue

    # As a final attempt, look for a JSON object in the full HTML that contains pageProps
    m = re.search(r"(\{.*\"pageProps\".*\})", html, flags=re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass

    return None


def extract_verses_from_fragment(fragment: str) -> Dict[str, str]:
    """Extract verses from HTML fragment."""
    soup = BeautifulSoup(fragment, "html.parser")
    verses: Dict[str, str] = {}
    # Primary selector: elements with data-usfm attribute
    elems = soup.find_all(attrs={"data-usfm": True})
    if not elems:
        # Fallback: sometimes attribute name differs (data-verse) or verses are in elements with class 'verse'
        elems = soup.find_all(attrs={"data-verse": True}) or soup.find_all(class_=re.compile(r"verse"))

    for el in elems:
        key = el.get("data-usfm") or el.get("data-verse")
        # Prefer well-structured inner elements with a 'content' class, otherwise fall back to full text
        contents = [c.get_text(" ", strip=True) for c in el.find_all(class_=re.compile(r"content"))]
        text = " ".join([c for c in contents if c]).strip()
        if not text:
            text = el.get_text(" ", strip=True)
            text = re.sub(r"^\d+\s+", "", text)
        if key:
            verses[key] = text
        else:
            # Try to build a key from the element's id or surrounding header if available
            el_id = el.get("id")
            if el_id and re.search(r"\d+$", el_id):
                verses[el_id] = text
    return verses
    return verses


def fetch_verse_pairs(book: str, chapter: int) -> List[Tuple[str, str, str]]:
    """Fetch and extract verse pairs for a chapter.
    
    Returns list of tuples: (usfm_key, urhobo_text, english_text)
    """
    html = fetch_chapter_html(book, chapter)
    if not html:
        return []

    data = extract_next_data(html)
    if not data:
        return []

    props = data.get("props", {}).get("pageProps", {})
    
    # Extract main (Urhobo) and parallel (English) fragments
    main_fragment = None
    parallel_fragment = None
    
    if props.get("chapterInfo") and isinstance(props["chapterInfo"], dict):
        main_fragment = props["chapterInfo"].get("content")
    if props.get("parallelChapterInfoData") and isinstance(props["parallelChapterInfoData"], dict):
        parallel_fragment = props["parallelChapterInfoData"].get("content")

    if not (main_fragment and parallel_fragment):
        # Try alternative keys that some pages use
        if not main_fragment and isinstance(props.get("chapter"), dict):
            main_fragment = props["chapter"].get("content")
        if not parallel_fragment and isinstance(props.get("parallelChapter"), dict):
            parallel_fragment = props["parallelChapter"].get("content")

        if not (main_fragment and parallel_fragment):
            # Log available keys to help debugging
            print(f"Missing fragments for {book} {chapter}; pageProps keys: {list(props.keys())}")
            return []

    main_verses = extract_verses_from_fragment(main_fragment)
    parallel_verses = extract_verses_from_fragment(parallel_fragment)

    # Create pairs, sorted by verse number
    pairs = []
    keys = sorted(set(main_verses.keys()) | set(parallel_verses.keys()), 
                  key=lambda k: int(re.search(r"(\d+)$", k).group(1)) if re.search(r"(\d+)$", k) else 0)
    
    for key in keys:
        urhobo = main_verses.get(key, "").strip()
        english = parallel_verses.get(key, "").strip()
        if urhobo and english:
            pairs.append((key, urhobo, english))

    return pairs


def main():
    """Main entry point."""
    print(f"Fetching parallel verse pairs (target: {TARGET_PAIRS})...\n")
    
    all_pairs = []
    
    for book in BOOKS.keys():
        if len(all_pairs) >= TARGET_PAIRS:
            break
        
        for chapter in range(1, BOOKS[book] + 1):
            if len(all_pairs) >= TARGET_PAIRS:
                break
            
            print(f"Fetching {book} {chapter}...", end=" ", flush=True)
            pairs = fetch_verse_pairs(book, chapter)
            
            if pairs:
                all_pairs.extend(pairs)
                print(f"✓ ({len(pairs)} verses, total: {len(all_pairs)})")
            else:
                print("✗ (no verses found)")
            
            # Be respectful to the server
            time.sleep(0.5)

    # Trim to target count
    all_pairs = all_pairs[:TARGET_PAIRS]
    
    # Write to CSV
    output_path = Path(OUTPUT_FILE)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["usfm", "urhobo", "english"])
        for usfm, urhobo, english in all_pairs:
            writer.writerow([usfm, urhobo, english])
    
    print(f"\n✓ Saved {len(all_pairs)} verse pairs to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())