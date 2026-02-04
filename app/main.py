from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

from .database import (
    get_db,
    init_db,
    save_analysis,
    get_analysis_by_id,
    get_all_analyses,
)
from .ai_service import analyze_job_description

# Create FastAPI app
app = FastAPI(title="Job Skill Analyzer API")


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("Database initialized")


# TODO: Define request/response models using Pydantic
class AnalysisResponse(BaseModel):
    id: int
    company_name: Optional[str]
    required_skills: List[str]
    preferred_skills: List[str]
    technologies: List[str]
    experience_level: str
    summary: str
    created_at: str


class AnalyzeRequest(BaseModel):
    job_description: str
    company_name: Optional[str] = None


# TODO: POST /api/analyze endpoint
@app.post("/api/analyze")
def analyze_endpoint(request: AnalyzeRequest):
    """
    Analyzes a job description and returns structured data.
    """
    job_desc = request.job_description
    company = request.company_name.strip() if request.company_name else None

    analysis_result = analyze_job_description(job_desc, company)

    saved_id = save_analysis(job_desc, company, analysis_result)

    full_analysis = get_analysis_by_id(saved_id)

    response = {
        "id": full_analysis["id"],
        "company_name": full_analysis["company_name"],
        "created_at": full_analysis["created_at"],
        **full_analysis["result"],
    }

    return response


# TODO: GET /api/history endpoint
@app.get("/api/history")
def get_history():
    """
    Returns all past analyses.
    """
    analyses = get_all_analyses()
    return analyses


# TODO: GET /api/analysis/{id} endpoint
@app.get("/api/analysis/{id}")
def get_single_analysis(id: int):
    """
    Returns a single analysis by ID.
    """
    analysis = get_analysis_by_id(id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    response = {
        "id": analysis["id"],
        "company_name": analysis["company_name"],
        "created_at": analysis["created_at"],
        **analysis["result"],
    }

    return response
