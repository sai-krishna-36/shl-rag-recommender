from pathlib import Path
import pickle
from sentence_transformers import SentenceTransformer

from data_loader import load_assessments

# Paths and config

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.pkl"

MODEL_NAME = "all-MiniLM-L6-v2"


# Embedding logic

def build_embeddings():
    """
    Loads SHL assessments and generates embeddings for assessment names.
    """
    assessments = load_assessments()
    model = SentenceTransformer(MODEL_NAME)

    texts = [a["name"] for a in assessments]
    embeddings = model.encode(texts, show_progress_bar=True)

    return assessments, embeddings


def save_embeddings(data, vectors):
    """
    Saves embeddings and metadata to disk.
    """
    DATA_DIR.mkdir(exist_ok=True)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(
            {
                "data": data,
                "embeddings": vectors
            },
            f
        )


# Manual run 

if __name__ == "__main__":
    data, vectors = build_embeddings()
    save_embeddings(data, vectors)
    print(f"Saved embeddings for {len(data)} assessments")
