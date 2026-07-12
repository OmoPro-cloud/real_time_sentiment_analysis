#!/usr/bin/env python3
"""Generate a parallel corpus CSV from a saved YouVersion chapter HTML file.

Usage:
    python open/generate_parallel.py 
    python open/generate_parallel.py --input open/bible_source.html --output open/parallel_corpus.csv

This script extracts the main version and the parallel version (if present)
from the embedded `__NEXT_DATA__` JSON and writes a CSV with columns:
  usfm, <MAIN_TITLE>, <PARALLEL_TITLE>

Requires: beautifulsoup4
    pip install beautifulsoup4
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, Optional

from bs4 import BeautifulSoup

# Default source URL (used when fetching instead of reading a local file)
BASE_SOURCE_URL = "https://www.bible.com/bible/2616/GEN.1.UBV77?parallel=114"


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch HTML from the given URL. Returns text or None on failure."""
    try:
        import requests

        headers = {"User-Agent": "generate_parallel/1.0 (+https://github.com)"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except ImportError:
        print("The 'requests' package is required to fetch remote URLs. Install with: pip install requests")
    except Exception as exc:  # pragma: no cover - network error handling
        print(f"Failed to fetch {url}: {exc}")
    return None


def load_next_data(html: str) -> Optional[dict]:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
    if not tag:
        return None
    try:
        return json.loads(tag.string)
    except Exception:
        return None


def extract_verses_from_fragment(fragment: str) -> Dict[str, str]:
    """Return mapping from verse key (data-usfm) -> text content."""
    soup = BeautifulSoup(fragment, "html.parser")
    verses: Dict[str, str] = {}
    # Prefer elements that carry a data-usfm attribute
    for el in soup.find_all(attrs={"data-usfm": True}):
        key = el.get("data-usfm")
        # find all content spans inside this element
        contents = [c.get_text(" ", strip=True) for c in el.find_all(class_=re.compile(r"content"))]
        text = " ".join([c for c in contents if c]).strip()
        if not text:
            # fallback to the element text without the label number
            text = el.get_text(" ", strip=True)
            # drop leading label if present
            text = re.sub(r"^\d+\s+", "", text)
        if key:
            verses[key] = text
    # if none found, try to find elements with class like 'verse v1'
    if not verses:
        for el in soup.select("span.verse, div.verse, span[class*=v]"):
            key = el.get("data-usfm") or (el.get("id") if el.get("id") else (".".join(el.get("class")) if el.get("class") else None))
            text = el.get_text(" ", strip=True)
            if key:
                verses[key] = re.sub(r"^\d+\s+", "", text)
    return verses


def sort_usfm_keys(keys):
    def key_fn(k: str):
        # try to find final numeric part
        m = re.search(r"(\d+)$", k)
        if m:
            return int(m.group(1))
        # fallback preserve original
        return k

    return sorted(keys, key=key_fn)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", default="open/bible_source.html", help="Path to saved chapter HTML (local cache)")
    p.add_argument("--output", "-o", default="open/parallel_corpus.csv", help="CSV output path")
    p.add_argument("--url", "-u", default=BASE_SOURCE_URL, help="Source chapter URL to fetch (default built-in)")
    p.add_argument("--fetch", action="store_true", help="Fetch HTML from the URL even if local file exists")
    p.add_argument("--save-cache", action="store_true", help="Save fetched HTML to the local input path for reuse")
    args = p.parse_args()

    html_path = Path(args.input)

    html = None
    # Decide whether to fetch from URL or use local file
    if args.fetch or not html_path.exists():
        print(f"Fetching HTML from {args.url} ...")
        fetched = fetch_url(args.url)
        if fetched:
            html = fetched
            if args.save_cache:
                html_path.parent.mkdir(parents=True, exist_ok=True)
                html_path.write_text(fetched, encoding="utf-8")
                print(f"Saved fetched HTML to {html_path}")
        else:
            if html_path.exists():
                print("Fetch failed — falling back to local file.")
                html = html_path.read_text(encoding="utf-8")
            else:
                print("Fetch failed and no local file available. Exiting.")
                return 2
    else:
        html = html_path.read_text(encoding="utf-8")

    data = load_next_data(html)
    if not data:
        print("Could not find embedded __NEXT_DATA__ JSON in the file. Exiting.")
        return 3

    props = data.get("props", {}).get("pageProps", {})

    # main chapter HTML
    main_fragment = None
    parallel_fragment = None
    # prefer chapterInfo.content if present
    if props.get("chapterInfo") and isinstance(props["chapterInfo"], dict):
        main_fragment = props["chapterInfo"].get("content")
    # parallel info
    if props.get("parallelChapterInfoData") and isinstance(props["parallelChapterInfoData"], dict):
        parallel_fragment = props["parallelChapterInfoData"].get("content")

    # titles
    main_title = "main"
    parallel_title = "parallel"
    if isinstance(props.get("versionData"), dict):
        main_title = props["versionData"].get("local_abbreviation") or props["versionData"].get("local_title") or main_title
    if isinstance(props.get("parallelVersionData"), dict):
        parallel_title = props["parallelVersionData"].get("local_abbreviation") or props["parallelVersionData"].get("local_title") or parallel_title
    # fallback: parallelChapterInfoData may be under different path
    if not parallel_fragment:
        parallel_fragment = props.get("parallelChapterInfoData", {}).get("content") if isinstance(props.get("parallelChapterInfoData"), dict) else None

    main_verses = extract_verses_from_fragment(main_fragment or "") if main_fragment else {}
    parallel_verses = extract_verses_from_fragment(parallel_fragment or "") if parallel_fragment else {}

    # union keys
    keys = list(set(list(main_verses.keys()) + list(parallel_verses.keys())))
    if not keys:
        print("No verses found in the document.")
        return 4

    ordered = sort_usfm_keys(keys)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    header = ["usfm", str(main_title)]
    if parallel_verses:
        header.append(str(parallel_title))

    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for k in ordered:
            row = [k, main_verses.get(k, "")]
            if parallel_verses:
                row.append(parallel_verses.get(k, ""))
            writer.writerow(row)

    print(f"Wrote {out_path} with {len(ordered)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
