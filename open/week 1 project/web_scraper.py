from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://www.bible.com/bible/2616/GEN.{chapter}.UBV77?parallel=114"

MAX_CHAPTERS = 50
TARGET_PAIRS = 1000

OUTPUT_FILE = "parallel_pairs.csv"


#start web driver

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# create csv file with  language pairs
if not os.path.exists(OUTPUT_FILE):
    df = pd.DataFrame(columns=["urhobo", "english"])
    df.to_csv(OUTPUT_FILE, index=False)


#

def scrape_chapter(chapter):

    url = BASE_URL.format(chapter=chapter)

    print(f"\nOpening chapter {chapter}")
    print(url)

    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    spans = soup.find_all("span")

    text_lines = []

    for span in spans:
        text = span.get_text(strip=True)

        if len(text) > 2:
            text_lines.append(text)

    # remove duplicates
    seen = set()
    cleaned = []

    for line in text_lines:
        if line not in seen:
            cleaned.append(line)
            seen.add(line)

    for i, line in enumerate(cleaned[:100]):
        print(i, repr(line))

    midpoint = len(cleaned) // 2

    urhobo = cleaned[:midpoint]
    english = cleaned[midpoint:]

    pairs = []

    for i in range(min(len(urhobo), len(english))):
        pairs.append({
            "urhobo": urhobo[i],
            "english": english[i]
        })

    print("Pairs found:", len(pairs))

    return pairs

#main loop

total_pairs = 0

for chapter in range(1, MAX_CHAPTERS + 1):

    try:

        chapter_pairs = scrape_chapter(chapter)

        # save each batch immediately
        df = pd.DataFrame(chapter_pairs)

        df.to_csv(
            OUTPUT_FILE,
            mode="a",          # append mode
            header=False,      # don't rewrite headers
            index=False
        )

        total_pairs += len(chapter_pairs)

        print("Saved to CSV:", total_pairs)

        if total_pairs >= TARGET_PAIRS:
            print("Reached 1000 pairs.")
            break

    except Exception as e:

        print("Error:", e)
        continue


driver.quit()

print("\nDone.")
print("Saved file:", OUTPUT_FILE)
print("Total pairs:", total_pairs)