"""Sports predictions router."""
from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from app.dependencies import get_current_user_optional
from app.models import User
from app.schemas import SportsPrediction
from app.services.external_apis import TheOddsAPI
from app.services.prediction_models import SportsPredictionModel
from app.database import get_mongodb

router = APIRouter(prefix="/sports", tags=["sports"])


@router.get("/predictions", response_model=List[SportsPrediction])
async def get_sports_predictions(
    sport: str = Query(default="basketball_nba", description="Sport key (e.g., basketball_nba, americanfootball_nfl)"),
    markets: str = Query(default="h2h", description="Comma-separated markets"),
    regions: str = Query(default="us", description="Comma-separated regions"),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get sports predictions for upcoming events.
    
    Args:
        sport: Sport key
        markets: Comma-separated markets
        regions: Comma-separated regions
        current_user: Authenticated user (optional)
        
    Returns:
        List of sports predictions
    """
    try:
        # Fetch odds data from The Odds API
        odds_data = await TheOddsAPI.get_sports_odds(sport, markets, regions)
        
        predictions = []
        mongodb = await get_mongodb()
        
        # Generate predictions for each event
        for event in odds_data[:10]:  # Limit to 10 events
            try:
                prediction_result = SportsPredictionModel.predict(event)
                
                # Log prediction
                await mongodb["prediction_logs"].insert_one({
                    "prediction_type": "sports",
                    "event_id": event.get("id", ""),
                    "prediction": prediction_result,
                    "timestamp": event.get("commence_time"),
                    "user_id": current_user.id if current_user else None
                })
                
                predictions.append(SportsPrediction(
                    event_id=event.get("id", ""),
                    prediction_type="sports",
                    probability=prediction_result["probability"],
                    confidence=prediction_result["confidence"],
                    outcome=prediction_result["outcome"],
                    team=prediction_result.get("team"),
                    odds=prediction_result.get("odds"),
                    implied_probability=prediction_result.get("implied_probability"),
                    model_version=prediction_result["model_version"],
                    metadata=prediction_result.get("metadata", {})
                ))
            except Exception as e:
                # Skip events that fail to process
                continue
        
        return predictions
        
    except Exception as e:
        # Return empty list on error rather than raising
        return []
