from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.schemas import ExamEvaluationRequest, ExamRubricScore
from ..services.exam_service import exam_service

router = APIRouter(prefix="/api/exam", tags=["Exam Prep & Evaluation"])

@router.get("/prompts", response_model=List[Dict[str, Any]])
async def get_exam_prompts():
    """Returns curated exam prompts for IELTS Cue Card, Job Interview, GD, and JAM."""
    return exam_service.get_all_prompts()

@router.post("/evaluate", response_model=ExamRubricScore)
async def evaluate_exam_submission(request: ExamEvaluationRequest):
    """Evaluates candidate speaking response across IELTS/Job Interview rubrics."""
    try:
        return await exam_service.evaluate_exam(
            exam_type=request.exam_type,
            topic=request.topic,
            transcript=request.transcript,
            time_taken=request.time_taken_seconds
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exam evaluation error: {str(e)}")
