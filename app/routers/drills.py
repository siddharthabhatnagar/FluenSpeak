from fastapi import APIRouter
from typing import List, Dict, Any
from ..models.schemas import DrillQuestion, DrillEvaluationRequest
from ..services.analytics_service import analytics_service

router = APIRouter(prefix="/api/drills", tags=["Weakness Drills"])

@router.get("/questions", response_model=List[DrillQuestion])
async def get_practice_drills():
    """Generates targeted grammar & fluency quizzes based on common speaking mistakes."""
    return analytics_service.generate_personalized_drills()

@router.post("/verify")
async def verify_drill_answer(submission: DrillEvaluationRequest) -> Dict[str, Any]:
    """Evaluates drill selection and returns immediate learning feedback."""
    questions = analytics_service.generate_personalized_drills()
    matched = next((q for q in questions if q.id == submission.question_id), None)
    
    if not matched:
        is_correct = submission.selected_option_index == 1
        return {
            "correct": is_correct,
            "explanation": "Great practice! Always be mindful of standard subject-verb agreements and tense consistency."
        }
        
    is_correct = submission.selected_option_index == matched.correct_option_index
    return {
        "correct": is_correct,
        "correct_option_index": matched.correct_option_index,
        "explanation": matched.explanation,
        "rule_category": matched.rule_category
    }
