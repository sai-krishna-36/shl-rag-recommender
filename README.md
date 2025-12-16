SHL Assessment Recommendation System
Overview
This project recommends suitable SHL assessments based on a user’s hiring or role-related query. It uses semantic similarity to match natural language queries with relevant SHL assessment products.
How It Works :
SHL assessment catalog data is scraped and cleaned
Assessment names are converted into vector embeddings
A user query is matched against these embeddings using similarity search
Results are filtered and balanced between technical and behavioral assessments
Recommendations are returned through a FastAPI backend

API Endpoints :
Health Check
GET /health

Get Recommendations:
POST /recommend

Request:
{
  "query": "Hiring a Java developer with good communication skills"
}

Tech Stack :
Python
FastAPI
SentenceTransformers
NumPy
Uvicorn
Evaluation

The system is evaluated using Mean Recall@10 on a provided labeled dataset. URL normalization is applied to handle differences between catalog and training data formats.

Deployment

The application is deployed as a FastAPI service and can be run using:

uvicorn backend.main:app

Notes

This project focuses on building a simple, explainable recommendation pipeline rather than heavy model tuning or complex ranking logic.



