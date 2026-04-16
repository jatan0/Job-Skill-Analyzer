from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

from .database import (
    init_db,
    save_analysis,
    get_analysis_by_id,
    get_all_analyses,
)
from .ai_service import analyze_job_description

app = FastAPI(title="Job Skill Analyzer API")


@app.on_event("startup")
def startup_event():
    init_db()


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
    job_description: str = Field(..., min_length=1)
    company_name: Optional[str] = None


@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze_endpoint(request: AnalyzeRequest):
    """
    Analyzes a job description and returns structured data
    """
    try:
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

    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=500, detail="AI processing error")

    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected internal server error")


@app.get("/api/history", response_model=List[AnalysisResponse])
def get_history():
    """
    Returns all past analyses.
    """
    analyses = get_all_analyses()

    response = []
    for analysis in analyses:
        response.append(
            {
                "id": analysis["id"],
                "company_name": analysis["company_name"],
                "created_at": analysis["created_at"],
                **analysis["result"],
            }
        )

    return response


@app.get("/api/analysis/{id}", response_model=AnalysisResponse)
def get_single_analysis(id: int):
    """
    Returns a single analysis by ID
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
