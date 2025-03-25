# app/routers/auth_router.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict, Any

from app.core.database import get_database
from app.schemas.user_schemas import UserResponse # or create new AuthResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# JWT Settings (Move these to app/core/settings.py)
SECRET_KEY = "YOUR_SECRET_KEY"  # IMPORTANT:  Change this to a strong, random string and store it securely!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

# Dependency to get the user from the database based on username
async def get_user_by_username(username: str, db):
    user = await db["users"].find_one({"username": username})  # AWAIT HERE
    if user is None:
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Authentication endpoint
@router.post("/auth/login", response_model=Dict[str, Any])  # Update with appropriate response model
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_database)):
    """
    Authenticates a user and returns a JWT token.
    """
    logger.info("Entering /auth/login (POST) endpoint")

    user = await get_user_by_username(form_data.username, db)  # AWAIT HERE TOO

    if not user:
        logger.warning(f"Login failed: User '{form_data.username}' not found")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if user["password"] != form_data.password: # VERY INSECURE - Plain text comparison
        logger.warning(f"Login failed: Incorrect password for user '{form_data.username}'")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Assuming you have role information in your 'roles' collection/table
    role = await db["roles"].find_one({"id": user["role_id"]})  # AWAIT the role query

    if not role:
       logger.error(f"Role not found for role_id: {user['role_id']}")
       raise HTTPException(status_code=500, detail="Internal Server Error: Role not found")

    access_token_data = {
        "sub": user["username"],  # Subject (typically username or user ID)
        "role_id": user["role_id"],
        "role_name": role["role"] # Added the role name in token
    }
    access_token = create_access_token(access_token_data) #create the token

    logger.info(f"User '{form_data.username}' logged in successfully")

    # Modify UserResponse or create a new AuthResponse model to include the token and role name
    return {
        "username": user["username"],
        "email": user["email"],
        "access_token": access_token,
        "token_type": "bearer",
        "role": {"id": user["role_id"], "name": role["role"]}
    }
