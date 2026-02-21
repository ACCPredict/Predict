"""FastAPI dependencies for authentication and database access."""
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db, get_mongodb
from app.auth import verify_clerk_token, get_user_id_from_token


async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Dependency to get current authenticated user.
    
    Validates Clerk JWT token and returns user information.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    token_payload = await verify_clerk_token(authorization)
    clerk_id = get_user_id_from_token(token_payload)
    
    # Get or create user in database
    from app.models import User
    user = db.query(User).filter(User.clerk_id == clerk_id).first()
    
    if not user:
        # Create new user if doesn't exist
        user = User(
            clerk_id=clerk_id,
            email=token_payload.get("email", f"{clerk_id}@example.com")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user


async def get_current_user_optional(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Optional dependency to get current authenticated user.
    
    Returns None if no authorization header is provided.
    """
    if not authorization:
        return None
    
    try:
        token_payload = await verify_clerk_token(authorization)
        clerk_id = get_user_id_from_token(token_payload)
        
        # Get or create user in database
        from app.models import User
        user = db.query(User).filter(User.clerk_id == clerk_id).first()
        
        if not user:
            # Create new user if doesn't exist
            user = User(
                clerk_id=clerk_id,
                email=token_payload.get("email", f"{clerk_id}@example.com")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        return user
    except Exception:
        # Return None if token verification fails
        return None
