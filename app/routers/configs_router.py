from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Body
from typing import List, Optional, Dict
from app.core.database import get_database
from app.models.config_model import Config
from app.core.auth import check_permission
from datetime import datetime
from app.schemas.user_schemas import UserResponse
from app.core.security import get_current_user
from app.schemas.config_schema import ConfigListResponse, ConfigResponse
import json

router = APIRouter()


@router.post(
    "/configs/",
    response_model=Config, 
    status_code=201,
    dependencies=[Depends(check_permission)],
    name="create_config")
async def create_config(
    name: str = Query(..., description="Name of the configuration"),
    device_name: str = Query(..., description="Device name"),
    config_data: Dict = Body(..., description="Configuration data (JSON object)"),
    db = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
):
    """Creates a new configuration."""

    # Validate device existence
    if not await db["devices"].find_one({"name": device_name}):
        raise HTTPException(status_code=400, detail="Device not found")

    # Check for duplicate config name
    if await db["configs"].find_one({"name": name}):
        raise HTTPException(status_code=400, detail="Configuration name already exists")

    config = Config(
        name=name,
        device_name=device_name,
        config_data=config_data,
        created_by=current_user.username,
        created_at=datetime.now()
        )
    config_dict = config.model_dump(exclude={"id"})
    result = await db["configs"].insert_one(config_dict)
    new_config = await db["configs"].find_one({"_id": result.inserted_id})
    new_config["_id"] = str(new_config["_id"])
    return Config(**new_config)

@router.post(
    "/configs/file/",
    response_model=Config,
    status_code=201,
    dependencies=[Depends(check_permission)],
    name="create_config_from_file"
    )
async def create_config_from_file(
    name: str = Query(..., description="Name of the configuration"),
    device_name: str = Query(..., description="Device name"),
    file: UploadFile = File(..., description="Configuration file"),
    db = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
):
    """Creates a new configuration from a file upload."""

    # Validate device existence
    if not await db["devices"].find_one({"name": device_name}):
        raise HTTPException(status_code=400, detail="Device not found")

    # Check for duplicate config name
    if await db["configs"].find_one({"name": name}):
        raise HTTPException(status_code=400, detail="Configuration name already exists")

    try:
        contents = await file.read()
        config_data = contents.decode()
        config_data = json.loads(config_data)  # Use json.loads()
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

    config = Config(
        name=name,
        device_name=device_name,
        config_data=config_data,
        created_by=current_user.username,
        created_at=datetime.now()
        )
    config_dict = config.model_dump(exclude={"id"})
    result = await db["configs"].insert_one(config_dict)
    new_config = await db["configs"].find_one({"_id": result.inserted_id})
    new_config["_id"] = str(new_config["_id"])
    return Config(**new_config)

@router.get(
    "/configs/",
    response_model=List[ConfigListResponse],
    dependencies=[Depends(check_permission)],
    name="list_configs"
    )
async def list_configs(db = Depends(get_database)):
    """Lists all configurations."""
    configs = []
    async for config in db["configs"].find():
        config["_id"] = str(config["_id"])
        configs.append(ConfigListResponse(**config))
    return configs

@router.get(
    "/configs/by-customer/{customer_name}",
    response_model=List[ConfigListResponse],
    dependencies=[Depends(check_permission)],
    name="list_configs_by_customer"
    )
async def list_configs_by_customer(
    customer_name: str,
    db = Depends(get_database)
    ):
    """Lists configurations for a specific customer."""
    configs = []
    # Find devices with matching customer_name
    async for device in db["devices"].find({"customer_name": customer_name}):
        device_name = device["name"]
        # Find configs with matching device_name
        async for config in db["configs"].find({"device_name": device_name}):
            config["_id"] = str(config["_id"])
            configs.append(ConfigListResponse(**config))
    return configs

@router.get(
    "/configs/by-user/{created_by}",
    response_model=List[ConfigListResponse],
    dependencies=[Depends(check_permission)],
    name="list_configs_by_user"
    )
async def list_configs_by_user(
    created_by: str,  # Use the correct name, and path parameter name
    db = Depends(get_database)
    ):
    """Lists configurations created by a specific user."""
    configs = []
    async for config in db["configs"].find({"created_by": created_by}):
        config["_id"] = str(config["_id"])
        configs.append(ConfigListResponse(**config))
    return configs


@router.put(
    "/configs/{name}",
    response_model=Config,
    dependencies=[Depends(check_permission)],
    name="update_config"
    )
async def update_config(
    name: str,
    new_name: str = Query(..., description="New name for the configuration"),
    device_name: Optional[str] = Query(None, description="New device name (optional)"),
    config_data: Optional[Dict] = Body(None, description="New configuration data (optional JSON object)"),
    db = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
):
    """Updates an existing configuration.  device_name and config_data are optional."""

    # Get existing configuration
    existing_config = await db["configs"].find_one({"name": name})
    if not existing_config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    # Check if the new config name already exists (excluding the config being updated)
    existing_config_with_new_name = await db["configs"].find_one({"name": new_name})
    if existing_config_with_new_name and existing_config_with_new_name["_id"] != existing_config["_id"]:
        raise HTTPException(status_code=400, detail="Configuration name already exists")

    # Validate device existence if a new device is provided
    if device_name and not await db["devices"].find_one({"name": device_name}):
        raise HTTPException(status_code=400, detail="Device not found")

    # Use existing values if new values are not provided
    updated_device_name = device_name if device_name is not None else existing_config["device_name"]
    updated_config_data = config_data if config_data is not None else existing_config["config_data"]


    config_dict = {
        "name": new_name,
        "device_name": updated_device_name,
        "config_data": updated_config_data,
        "created_by": current_user.username,
        "created_at": datetime.now()
        }

    update_result = await db["configs"].update_one({"name": name}, {"$set": config_dict})

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")

    updated_config = await db["configs"].find_one({"name": new_name})
    updated_config["_id"] = str(updated_config["_id"])
    return Config(**updated_config)

@router.delete(
    "/configs/{name}",
    status_code=204,
    dependencies=[Depends(check_permission)],
    name="delete_config"
    )
async def delete_config(name: str, db = Depends(get_database)):
    """Deletes a configuration."""
    delete_result = await db["configs"].delete_one({"name": name})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return None
