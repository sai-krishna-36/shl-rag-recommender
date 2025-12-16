from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from backend.retriever import balanced_recommend

app = FastAPI(title="SHL Assessment Recommendation API")
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class RecommendRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
def home():
    index_file = FRONTEND_DIR / "index.html"
    return index_file.read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(req: RecommendRequest):
    results = balanced_recommend(req.query, top_k=10)

    return {
        "query": req.query,
        "recommendations": [
            {
                "assessment_name": r["name"],
                "assessment_url": r["url"]
            }
            for r in results
        ]
    }