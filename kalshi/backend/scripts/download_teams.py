from pathlib import Path

RAW_DATA = Path(".../data/raw")

def main():
    RAW_DATA.mkdir(parents=True, exist_ok=True)

    print("Raw data folder exists.")

if __name__ == "__main__":
    main()

#this file is responsible for contacting the data source, downloading the newest dataset and storing it in raw/