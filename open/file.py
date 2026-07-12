import requests
from bs4 import BeautifulSoup


BASE_URL_TEMPLATE = "https://www.bible.com/bible/2616/{BOOK}.{CHAPTER}.UBV77?parallel=114"

def fetch_chapter_html(book: str, chapter: int, timeout: int = 10):
    url = BASE_URL_TEMPLATE.format(BOOK=book, CHAPTER=chapter)
    print(f"Fetching URL: {url}")

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    html = fetch_chapter_html("GEN",1)

    if html:
        print("Raw HTML")
        print(html[:1000])
    else:
        print("no html found")

if __name__ == "__main__":
    main()