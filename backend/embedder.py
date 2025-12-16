from sentence_transformers import SentenceTransformer
from data_loader import load_assessments
import pickle
from pathlib import Path

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = Path("data/embeddings.pkl")

def build_embeddings():
    assessments = load_assessments()
    model = SentenceTransformer(MODEL_NAME)

    texts = [a["name"] for a in assessments]
    embeddings = model.encode(texts, show_progress_bar=True)

    return assessments, embeddings

def save_embeddings(data, vectors):
    EMBEDDINGS_FILE.parent.mkdir(exist_ok=True)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump({
            "data": data,
            "embeddings": vectors
        }, f)

if __name__ == "__main__":
    data, vectors = build_embeddings()
    save_embeddings(data, vectors)

    print(f"Saved embeddings for {len(data)} assessments")
