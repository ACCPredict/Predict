"""Analytics router for accuracy metrics."""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.dependencies import get_current_user_optional, get_db
from app.models import User, AccuracyMetric
from app.schemas import AccuracyResponse
from app.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/accuracy", response_model=List[AccuracyResponse])
async def get_accuracy_metrics(
    prediction_type: Optional[str] = Query(None, description="Filter by prediction type (stock or sports)"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Get accuracy metrics for predictions.
    
    Args:
        prediction_type: Optional filter by type
        current_user: Authenticated user (optional)
        db: Database session
        
    Returns:
        List of accuracy metrics
    """
    query = db.query(AccuracyMetric)
    
    if prediction_type:
        query = query.filter(AccuracyMetric.prediction_type == prediction_type)
    
    metrics = query.all()
    
    return [
        AccuracyResponse(
            prediction_type=metric.prediction_type,
            model_version=metric.model_version,
            total_predictions=metric.total_predictions,
            correct_predictions=metric.correct_predictions,
            accuracy_rate=metric.accuracy_rate,
            last_updated=metric.last_updated
        )
        for metric in metrics
    ]
