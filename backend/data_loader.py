import csv
from pathlib import Path
DATA_FILE = Path("data/shl_assessments_clean.csv")
def load_assessments():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE} not found")

    assessments = []

    with DATA_FILE.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            assessments.append({
                "name": row["name"],
                "url": row["url"]
            })

    return assessments
if __name__ == "__main__":
    data = load_assessments()
    print(f"Loaded {len(data)} assessments")
