from pathlib import Path

RAW_DATA = Path(".../data/raw")
PROCESSED_DATA = Path(".../data/processed")

def main():
    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)

    print("Processed data folder exists.")

if __name__ == "__main__":
    main()

#this file is responsible fot removing duplicates, validating columns, fixing inconsistent name, handling missing values and exporting a clean dataset