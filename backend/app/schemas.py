"""Pydantic schemas for API request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PredictionBase(BaseModel):
    """Base prediction schema."""
    symbol: Optional[str] = None
    event_id: Optional[str] = None
    prediction_type: str  # 'stock' or 'sports'
    probability: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    metadata: Optional[Dict[str, Any]] = None


class StockPrediction(PredictionBase):
    """Stock prediction response."""
    symbol: str
    prediction_type: str = "stock"
    direction: str  # 'up' or 'down'
    price_target: Optional[float] = None
    current_price: Optional[float] = None


class SportsPrediction(PredictionBase):
    """Sports prediction response."""
    event_id: str
    prediction_type: str = "sports"
    team: Optional[str] = None
    outcome: str  # 'win', 'loss', 'over', 'under', etc.
    odds: Optional[float] = None
    implied_probability: Optional[float] = None


class UserPickCreate(BaseModel):
    """Schema for creating a user pick."""
    prediction_type: str
    symbol_or_event: str
    prediction: Dict[str, Any]
    confidence: float = Field(..., ge=0.0, le=1.0)


class UserPickResponse(BaseModel):
    """User pick response schema."""
    id: int
    prediction_type: str
    symbol_or_event: str
    prediction: Dict[str, Any]
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class AccuracyResponse(BaseModel):
    """Accuracy metrics response."""
    prediction_type: str
    model_version: str
    total_predictions: int
    correct_predictions: int
    accuracy_rate: float
    last_updated: datetime
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
