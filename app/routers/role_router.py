from fastapi import APIRouter, HTTPException, Depends, status, Query
from app.core.database import get_database
from app.models.role_model import Role
from app.schemas.role_schemas import RoleCreate, RoleResponse, RoleUpdate
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from typing import List, Optional
from app.core.auth import check_permission
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

def get_role_collection(db=Depends(get_database)) -> Collection:
    logger.debug("Entering get_role_collection function")
    db_instance = db["roles"]
    logger.debug(f"Returning role collection: {db_instance}")
    return db_instance

@router.get("/roles/list_roles", response_model=List[RoleResponse], name="list_roles",
            dependencies=[Depends(check_permission)])
async def list_roles(role_collection: Collection = Depends(get_role_collection)):
    """
    Lists all roles.
    """
    logger.info("Entering list_roles endpoint")
    try:
        logger.debug("Attempting to retrieve roles from the database")
        roles = []
        async for role_data in role_collection.find():  # Use async for loop
            logger.debug(f"Processing role_data: {role_data}")

            # Map database fields to Role model fields
            role = Role(
                id=str(role_data.get("id")),  # Convert int to string
                name=role_data.get("name"),  # Map 'role' field to 'name'
                description=role_data.get("description"),
            )
            logger.debug(f"Role model created: {role}")
            roles.append(RoleResponse(**role.dict()))  # type: ignore

        logger.info("Successfully listed roles.")
        logger.debug(f"Returning roles: {roles}")
        return roles
    except Exception as e:
        logger.exception(f"Error listing roles: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing roles: {e}")
    

@router.get("/roles/{role_id}", response_model=RoleResponse, name="read_role",
            dependencies=[Depends(check_permission)])
async def get_role(role_id: str, role_collection: Collection = Depends(get_role_collection)):
    """
    Retrieves a role by ID.
    """
    logger.info(f"Entering get_role endpoint with role_id: {role_id}")
    try:
        logger.debug(f"Attempting to retrieve role with ID: {role_id} from the database")
        role_data = await role_collection.find_one({"id": int(role_id)}) # Changed Query

        if role_data:
            logger.debug(f"Role found: {role_data}")
            # Map database fields to Role model fields
            role_model = Role(
                id=str(role_data["id"]),  # Convert int to string
                name=role_data["name"],  # Map 'role' field to 'name'
                description=role_data["description"],
            )
            logger.info("Successfully retrieved role.")
            return RoleResponse(**role_model.dict())  # type: ignore
        else:
            logger.warning(f"Role with ID: {role_id} not found")
            raise HTTPException(status_code=404, detail="Role not found")
    except Exception as e:
        logger.exception(f"Error retrieving role: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving role: {e}")
