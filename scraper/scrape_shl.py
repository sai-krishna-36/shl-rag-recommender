import requests
from bs4 import BeautifulSoup
import csv
import os
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

def scrape_all_pages(max_pages=15):
    all_assessments = []

    for page in range(1, max_pages + 1):
        url = f"{CATALOG_URL}?page={page}"
        print(f"Scraping page {page}...")

        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        found = 0

        for link in soup.find_all("a", href=True):
            href = link.get("href")
            name = link.get_text(strip=True)

            if not href or not name:
                continue

            if "/products/" in href and "job-solutions" not in href:
                all_assessments.append({
                    "name": name,
                    "url": BASE_URL + href
                })
                found += 1

        if found == 0:
            break  # no more products

        time.sleep(1)  # be polite

    return all_assessments

def save_to_csv(data):
    os.makedirs("data", exist_ok=True)
    path = "data/shl_assessments_raw.csv"

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url"])
        writer.writeheader()
        writer.writerows(data)

    return path

if __name__ == "__main__":
    results = scrape_all_pages()
    print(f"Total raw scraped: {len(results)}")
    save_to_csv(results)
