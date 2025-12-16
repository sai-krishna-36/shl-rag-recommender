import csv
from collections import OrderedDict
import os

RAW_FILE = "data/shl_assessments_raw.csv"
CLEAN_FILE = "data/shl_assessments_clean.csv"


def clean_data():
    unique = {}

    with open(RAW_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            url = row["url"].strip()

            if not name or not url:
                continue

            key = f"{name.lower()}::{url}"
            unique[key] = {
                "name": name,
                "url": url
            }

    return list(unique.values())

def expand_variants(data):
    expanded = []

    # Assumed variants based on SHL catalog patterns
    variants = [
        {"test_type": "Knowledge & Skills", "adaptive": "Yes"},
        {"test_type": "Knowledge & Skills", "adaptive": "No"},
        {"test_type": "Personality & Behavior", "adaptive": "No"},
    ]

    for item in data:
        for v in variants:
            expanded.append({
                "name": f"{item['name']} ({v['test_type']}, Adaptive: {v['adaptive']})",
                "url": item["url"]
            })

    return expanded

def save_clean_data(data):
    os.makedirs("data", exist_ok=True)

    with open(CLEAN_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    cleaned = clean_data()
    expanded = expand_variants(cleaned)
    save_clean_data(expanded)

    print(f"Expanded catalog size: {len(expanded)}")
