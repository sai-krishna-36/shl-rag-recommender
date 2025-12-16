import sys
sys.path.append("backend")

import csv
from collections import defaultdict
from retriever import balanced_recommend

TRAIN_FILE = "data/train.csv"

def normalize_url(url):
    return url.rstrip("/").split("/")[-1].lower()

def recall_at_k(predicted, actual, k=10):
    predicted_norm = {normalize_url(u) for u in predicted[:k]}
    actual_norm = {normalize_url(u) for u in actual}

    hits = len(predicted_norm & actual_norm)
    return hits / len(actual_norm) if actual_norm else 0.0

def load_ground_truth():
    truth = defaultdict(list)

    with open(TRAIN_FILE, encoding="cp1252") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = row["Query"].strip()
            url = row["Assessment_url"].strip()
            truth[query].append(url)

    return truth

def evaluate():
    ground_truth = load_ground_truth()
    scores = []

    for query, actual_urls in ground_truth.items():
        results = balanced_recommend(query, top_k=10)
        predicted_urls = [r["url"] for r in results]
        scores.append(recall_at_k(predicted_urls, actual_urls))

    mean_recall = sum(scores) / len(scores)
    print(f"Mean Recall@10: {mean_recall:.3f}")


if __name__ == "__main__":
    evaluate()
