'''import requests
from bs4 import BeautifulSoup

BASE_SOURCE_URL = "https://www.bible.com/bible/2616/GEN.1.UBV77?parallel=114"

response = requests.get(BASE_SOURCE_URL)
if response.status_code == 200:
    print("Successfully fetched the page!")
    #print(response.text[:500]) #prints first 500 characters of response
    soup = BeautifulSoup(response.text, 'lxml')
    print("Parsed the HTML content.")
    title = soup.find(class_='ChapterContent-module__cat7xG__heading').get_text()
    print(f"Title: {title}")'''

import requests
from bs4 import BeautifulSoup

BASE_SOURCE_URL = "https://www.bible.com/bible/2616/GEN.1.UBV77?parallel=114"

# Send request with browser-like headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(BASE_SOURCE_URL, headers=headers)

if response.status_code == 200:
    print("Successfully fetched the page!")

    soup = BeautifulSoup(response.text, "lxml")

    # Get title (Genesis 1)
    title = soup.find("h1")
    if title:
        print("Chapter:", title.get_text(strip=True))

    print("\nVerses 1-5:\n")

    # Find all verse spans/divs
    verses = soup.find_all(attrs={"data-usfm": True})

    # Loop through first 5 verses
    count = 0
    for verse in verses:
        verse_num = verse.get("data-usfm")

        # Example format: GEN.1.1
        if verse_num and verse_num.startswith("GEN.1."):
            num = verse_num.split(".")[-1]

            if int(num) <= 5:
                print(f"Verse {num}: {verse.get_text(strip=True)}")
                count += 1

        if count == 5:
            break

else:
    print("Failed to fetch page:", response.status_code)