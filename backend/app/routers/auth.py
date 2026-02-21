"""Authentication router for token verification."""
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/verify")
async def verify_auth(current_user: User = Depends(get_current_user)):
    """Verify authentication and return user info."""
    return {
        "authenticated": True,
        "user_id": current_user.id,
        "clerk_id": current_user.clerk_id,
        "email": current_user.email
    }
