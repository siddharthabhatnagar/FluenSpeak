from fastapi import APIRouter
from ..models.schemas import AnalyticsSummary
from ..services.analytics_service import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics & Progress"])

@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary():
    """Returns user's speaking stats, error pattern distributions, and weekly fluency trajectory."""
    return analytics_service.get_summary()
