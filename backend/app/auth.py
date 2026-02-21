"""Authentication utilities for Clerk JWT validation."""
import jwt
import httpx
from fastapi import HTTPException, status
from app.config import settings


async def verify_clerk_token(token: str) -> dict:
    """
    Verify Clerk JWT token and return decoded payload.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        # Get Clerk JWKS (JSON Web Key Set) for token verification
        async with httpx.AsyncClient() as client:
            # Clerk's JWKS endpoint (this is a simplified version)
            # In production, you'd fetch this from Clerk's API
            jwks_url = f"https://api.clerk.dev/v1/jwks"
            response = await client.get(jwks_url)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to verify token"
                )
        
        # For now, we'll use a simpler verification approach
        # In production, use proper JWKS verification
        # This is a placeholder - you should implement proper JWT verification
        # using Clerk's public keys
        
        # Decode without verification for development (NOT FOR PRODUCTION)
        # In production, use Clerk's SDK or proper JWT verification
        try:
            decoded = jwt.decode(
                token,
                options={"verify_signature": False}  # Remove in production
            )
            return decoded
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


def get_user_id_from_token(token_payload: dict) -> str:
    """Extract user ID (Clerk ID) from token payload."""
    # Clerk typically uses 'sub' for user ID
    return token_payload.get("sub") or token_payload.get("user_id")
