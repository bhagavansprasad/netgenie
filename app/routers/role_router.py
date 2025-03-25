from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_database
from app.models.role_model import Role
from app.schemas.role_schemas import RoleCreate, RoleResponse
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from typing import List

router = APIRouter()

def get_role_collection(db=Depends(get_database)) -> Collection:
    return db["roles"]

@router.post("/roles", response_model=RoleResponse, status_code=201)
async def create_role(role_create: RoleCreate, role_collection: Collection = Depends(get_role_collection)):
    """
    Creates a new role.
    """
    role_dict = role_create.dict()
    role_dict["created_at"] = datetime.utcnow()
    role_dict["updated_at"] = datetime.utcnow()

    try:
        result = role_collection.insert_one(role_dict)
        role_id = str(result.inserted_id)

        # Fetch the newly created role
        new_role = role_collection.find_one({"_id": result.inserted_id})
        if new_role:
            # Convert ObjectId to string for the response
            new_role["_id"] = str(new_role["_id"])
            role = Role(**new_role)  # type: ignore
            return RoleResponse(**role.dict())  # type: ignore
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve the newly created role")

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Role name already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating role: {e}")

@router.get("/roles", response_model=List[RoleResponse])
async def list_roles(role_collection: Collection = Depends(get_role_collection)):
    """
    Lists all roles.
    """
    try:
        roles = list(role_collection.find())

        role_list = []
        for role in roles:
            role["_id"] = str(role["_id"])
            role_model = Role(**role)  # type: ignore
            role_list.append(RoleResponse(**role_model.dict()))  # type: ignore

        return role_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing roles: {e}")

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: str, role_collection: Collection = Depends(get_role_collection)):
    """
    Retrieves a role by ID.
    """
    try:
        role = role_collection.find_one({"_id": role_id})

        if role:
            role["_id"] = str(role["_id"])
            role_model = Role(**role)  # type: ignore
            return RoleResponse(**role_model.dict())  # type: ignore
        else:
            raise HTTPException(status_code=404, detail="Role not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving role: {e}")
