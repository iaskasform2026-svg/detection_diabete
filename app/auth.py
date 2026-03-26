import os
from fastapi import Header, HTTPException, status

API_TOKEN = os.getenv("API_TOKEN", "change-me-in-production")


def verify_token(authorization: str | None = Header(default=None)) -> str:
    """Simple Bearer token verification.

    Expected header: Authorization: Bearer <token>
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing.",
        )

    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme.",
        )

    token = authorization[len(prefix):].strip()
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API token.",
        )
    return token
