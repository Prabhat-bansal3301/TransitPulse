
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db.device import get_active_device_by_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_device(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing device authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    if not token or len(token) > 512:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    device = get_active_device_by_token(token)

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive device.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return device
