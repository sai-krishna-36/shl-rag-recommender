import sys
import os
import csv

# ---- FIX PYTHON PATH ----
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from backend.retriever import balanced_recommend


INPUT_FILE = os.path.join("evaluation", "test.csv")
OUTPUT_FILE = "krishna_sai.csv"


def main():
    results = []

    # Read test CSV (IGNORE bad characters)
    with open(INPUT_FILE, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)

        for row in reader:
            query = row["Query"]

            recommendations = balanced_recommend(query, top_k=10)

            urls = [rec["url"] for rec in recommendations]

            results.append({
                "Query": query,
                "Predicted_Assessment_URLs": "|".join(urls)
            })

    # Write predictions
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Query", "Predicted_Assessment_URLs"]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Predictions saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
