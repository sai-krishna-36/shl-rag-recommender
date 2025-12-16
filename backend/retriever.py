import sys
from pathlib import Path
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Path setup (critical for Render) ---
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BASE_DIR / "data"

if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from embedder import build_embeddings, save_embeddings

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.pkl"


def load_embeddings():
    """
    Load embeddings if present.
    If missing, generate them at runtime (Render-safe).
    """
    if not EMBEDDINGS_FILE.exists():
        print("Embeddings not found. Generating embeddings...")
        data, vectors = build_embeddings()
        save_embeddings(data, vectors)
        print("Embeddings generated and saved.")

    with open(EMBEDDINGS_FILE, "rb") as f:
        payload = pickle.load(f)

    return payload["data"], payload["embeddings"]


def retrieve(query: str, top_k: int = 30):
    data, embeddings = load_embeddings()
    model = SentenceTransformer(MODEL_NAME)

    query_vec = model.encode([query])[0]
    scores = np.dot(embeddings, query_vec)

    top_indices = np.argsort(scores)[::-1][:top_k]
    return [data[i] for i in top_indices]


def balanced_recommend(query: str, top_k: int = 10):
    candidates = retrieve(query, top_k=40)

    tech, behavior = [], []
    blacklist = [
        "view all shl products",
        "ultimate view of potential"
    ]

    for item in candidates:
        name = item["name"].lower()
        if any(bad in name for bad in blacklist):
            continue

        if "personality" in name or "behavior" in name:
            behavior.append(item)
        else:
            tech.append(item)

    return (tech[:6] + behavior[:4])[:top_k]
