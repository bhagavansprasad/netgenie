from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.settings import settings  # Access your SECRET_KEY
from app.core.database import get_database
from typing import Dict, Any
from fastapi.openapi.utils import get_openapi
import logging
from app.schemas.user_schemas import UserResponse

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # URL of your login endpoint

async def get_user_from_db(db, username: str):
    """Retrieves a user from the database by username."""
    user = await db["users"].find_one({"username": username})
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_database)):
    """Retrieves the current user based on the JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_from_db(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    #  Construct UserResponse object instead of returning a dict
    return UserResponse(id=user["id"], username=user["username"], role_id=user["role_id"], email=user["email"])


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
