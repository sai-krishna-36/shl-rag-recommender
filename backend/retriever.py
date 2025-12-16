import sys
from pathlib import Path

# --- Ensure backend/ is on Python path ---
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = Path("data/embeddings.pkl")


def load_embeddings():
    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError("Embeddings file not found. Run embedder.py first.")

    with open(EMBEDDINGS_FILE, "rb") as f:
        payload = pickle.load(f)

    return payload["data"], payload["embeddings"]



def retrieve(query: str, top_k: int = 30):
    """
    Pure semantic retrieval using cosine similarity.
    """
    data, embeddings = load_embeddings()
    model = SentenceTransformer(MODEL_NAME)

    query_vec = model.encode([query])[0]
    scores = np.dot(embeddings, query_vec)

    top_indices = np.argsort(scores)[::-1][:top_k]
    return [data[i] for i in top_indices]


def balanced_recommend(query: str, top_k: int = 10):
    """
    Balanced recommendation:
    Filters junk entries
    Returns mix of technical + behavioral assessments
    """
    candidates = retrieve(query, top_k=40)

    tech = []
    behavior = []

    blacklist = [
        "view all shl products",
        "ultimate view of potential"
    ]

    for item in candidates:
        name_lower = item["name"].lower()

        # Remove junk / marketing links
        if any(bad in name_lower for bad in blacklist):
            continue

        if "personality" in name_lower or "behavior" in name_lower:
            behavior.append(item)
        else:
            tech.append(item)

    # 60% technical, 40% behavioral
    results = tech[:6] + behavior[:4]
    return results[:top_k]

# Local test

if __name__ == "__main__":
    query = "Hiring a Java developer who collaborates with stakeholders"
    results = balanced_recommend(query)

    for r in results:
        print(r["name"])
