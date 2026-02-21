"""User picks router."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models import User, UserPick
from app.schemas import UserPickCreate, UserPickResponse

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/picks", response_model=UserPickResponse, status_code=status.HTTP_201_CREATED)
async def create_user_pick(
    pick: UserPickCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save a user's prediction/pick.
    
    Args:
        pick: Pick data to save
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Created user pick
    """
    try:
        import json
        
        db_pick = UserPick(
            user_id=current_user.id,
            prediction_type=pick.prediction_type,
            symbol_or_event=pick.symbol_or_event,
            prediction=json.dumps(pick.prediction),
            confidence=pick.confidence
        )
        
        db.add(db_pick)
        db.commit()
        db.refresh(db_pick)
        
        return UserPickResponse(
            id=db_pick.id,
            prediction_type=db_pick.prediction_type,
            symbol_or_event=db_pick.symbol_or_event,
            prediction=json.loads(db_pick.prediction),
            confidence=db_pick.confidence,
            created_at=db_pick.created_at
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save pick: {str(e)}"
        )


@router.get("/picks", response_model=List[UserPickResponse])
async def get_user_picks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all picks for the current user.
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of user picks
    """
    import json
    
    picks = db.query(UserPick).filter(UserPick.user_id == current_user.id).all()
    
    return [
        UserPickResponse(
            id=pick.id,
            prediction_type=pick.prediction_type,
            symbol_or_event=pick.symbol_or_event,
            prediction=json.loads(pick.prediction),
            confidence=pick.confidence,
            created_at=pick.created_at
        )
        for pick in picks
    ]
