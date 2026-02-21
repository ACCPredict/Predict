"""SQLAlchemy models for PostgreSQL database."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model stored in PostgreSQL."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    picks = relationship("UserPick", back_populates="user")


class UserPick(Base):
    """User's saved predictions/picks."""
    __tablename__ = "user_picks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prediction_type = Column(String, nullable=False)  # 'stock' or 'sports'
    symbol_or_event = Column(String, nullable=False)  # Stock symbol or event ID
    prediction = Column(Text, nullable=False)  # JSON string of prediction
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="picks")


class AccuracyMetric(Base):
    """Accuracy metrics for predictions."""
    __tablename__ = "accuracy_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_type = Column(String, nullable=False)  # 'stock' or 'sports'
    model_version = Column(String, nullable=False)
    total_predictions = Column(Integer, default=0)
    correct_predictions = Column(Integer, default=0)
    accuracy_rate = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
