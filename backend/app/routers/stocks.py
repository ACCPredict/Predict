"""Stock predictions router."""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.dependencies import get_current_user_optional
from app.models import User
from app.schemas import StockPrediction
from app.services.external_apis import AlphaVantageAPI
from app.services.prediction_models import StockPredictionModel
from app.database import get_mongodb

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/predictions", response_model=StockPrediction)
async def get_stock_prediction(
    symbol: str = Query(..., description="Stock ticker symbol (e.g., AAPL, MSFT)"),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get stock prediction for a given symbol.
    
    Args:
        symbol: Stock ticker symbol
        current_user: Authenticated user (optional for this endpoint)
        
    Returns:
        Stock prediction with probability, confidence, and direction
    """
    try:
        # Fetch stock data from Alpha Vantage
        stock_data = await AlphaVantageAPI.get_stock_data(symbol.upper())
        
        # Generate prediction
        prediction_result = StockPredictionModel.predict(stock_data)
        
        # Log prediction to MongoDB
        mongodb = await get_mongodb()
        await mongodb["prediction_logs"].insert_one({
            "prediction_type": "stock",
            "symbol": symbol.upper(),
            "prediction": prediction_result,
            "timestamp": prediction_result.get("metadata", {}).get("timestamp"),
            "user_id": current_user.id if current_user else None
        })
        
        # Return prediction
        return StockPrediction(
            symbol=symbol.upper(),
            prediction_type="stock",
            probability=prediction_result["probability"],
            confidence=prediction_result["confidence"],
            direction=prediction_result["direction"],
            price_target=prediction_result.get("price_target"),
            current_price=prediction_result.get("current_price"),
            model_version=prediction_result["model_version"],
            metadata=prediction_result.get("metadata", {})
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate prediction: {str(e)}"
        )
