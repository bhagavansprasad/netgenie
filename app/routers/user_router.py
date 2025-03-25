from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
import logging
from app.core.database import get_database
from pymongo import MongoClient
from bson import ObjectId # not needed anymore since we are using sequential integer
from app.schemas.user_schemas import UserResponse
from pydantic import EmailStr

router = APIRouter()

logger = logging.getLogger(__name__)

async def get_next_sequence(db, sequence_name: str):
    """Atomically increments the sequence number in the 'counters' collection."""
    result = await db["counters"].find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True,  # Return the updated document
    )
    return result["seq"]

async def get_user(user_id: int, db):
    user = db["users"].find_one({"id": user_id}) # now we look for id
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(
    username: str = Query(..., title="Username", description="The username for the new user"),
    password: str = Query(..., title="Password", description="The password for the new user"),
    role_id: int = Query(..., title="Role ID", description="The role ID for the new user"),
    email: EmailStr = Query(..., title="Email", description="The email address for the new user"),
    db = Depends(get_database)
):
    """Create a new user (query parameters) with sequential integer ID."""
    logger.info("Entering /users/ (POST) endpoint (query parameters)")

    # Check if username or email already exists
    if db["users"].find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if db["users"].find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Get the next sequence number
    user_id = await get_next_sequence(db, "user_id") # get the autoincrementing sequence

    user_data = {
        "id": user_id,  # Use sequential integer ID
        "username": username,
        "password": password,  # Store plain text password (VERY INSECURE)
        "role_id": role_id,
        "email": email,
    }

    result = db["users"].insert_one(user_data) #insert one to the table

    logger.info(f"User created successfully with ID: {user_id}")
    new_user = await get_user(user_id, db)

    return UserResponse(id=new_user["id"], username=new_user["username"], role_id=new_user["role_id"], email=new_user["email"])


@router.get("/users/", response_model=List[UserResponse])
async def list_users(db = Depends(get_database)):
    """List all users."""
    logger.info("Entering /users/ (GET) endpoint")
    users = []
    for user in db["users"].find():
        users.append(UserResponse(id=user["id"], username=user["username"], role_id=user["role_id"], email=user["email"])) # converting object id to string
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db = Depends(get_database)): # changed to int
    """Read a user by ID."""
    logger.info(f"Entering /users/{user_id} (GET) endpoint")
    user = await get_user(user_id, db) # use helper to get the user
    return UserResponse(id=user["id"], username=user["username"], role_id=user["role_id"], email=user["email"])


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, #changed to int
    username: Optional[str] = Query(None, title="Username", description="The username for the new user"),
    password: Optional[str] = Query(None, title="Password", description="The password for the new user"),
    role_id: Optional[int] = Query(None, title="Role ID", description="The role ID for the new user"),
    email: Optional[EmailStr] = Query(None, title="Email", description="The email address for the new user"),
    db = Depends(get_database)
):
    """Update a user by ID (query parameters)."""
    logger.info(f"Entering /users/{user_id} (PUT) endpoint (query parameters)")

    user_data = {}
    if username is not None:
        user_data["username"] = username
    if password is not None:
        user_data["password"] = password # VERY INSECURE - Storing plain text
    if role_id is not None:
        user_data["role_id"] = role_id
    if email is not None:
        user_data["email"] = email

    if len(user_data) >= 1:
        # Check username and email duplication before updating
        existing_user = await get_user(user_id, db)
        if username and username != existing_user['username'] and db["users"].find_one({"username": username}):
            raise HTTPException(status_code=400, detail="Username already exists")
        if email and email != existing_user['email'] and db["users"].find_one({"email": email}):
            raise HTTPException(status_code=400, detail="Email already exists")

        update_result = db["users"].update_one(
            {"id": user_id}, {"$set": user_data} # now we look for id
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

    updated_user = await get_user(user_id, db)
    return UserResponse(id=updated_user["id"], username=updated_user["username"], role_id=updated_user["role_id"], email=updated_user["email"])


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db = Depends(get_database)): # change to int
    """Delete a user by ID."""
    logger.info(f"Entering /users/{user_id} (DELETE) endpoint")
    delete_result = db["users"].delete_one({"id": user_id}) # change to id
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None
