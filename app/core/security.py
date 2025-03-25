# app/core/security.py
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.settings import settings  # Access your SECRET_KEY
from app.core.database import get_database
from typing import Dict, Any
from fastapi.openapi.utils import get_openapi

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # URL of your login endpoint


async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_database)) -> Dict[str, Any]:  # Returns dictionary
    """
    Verifies the JWT token and returns the user information.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        role_id: int = payload.get("role_id")
        role_name: str = payload.get("role_name")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db["users"].find_one({"username": username}) # Or lookup by user ID, depending on your token

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username, "role_id": role_id, "role_name": role_name} #return the user info as dictionary


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="NetGenie API",
        version="0.1.0",
        description="Awesome netconfig generation API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}  # Add scopes as needed
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema