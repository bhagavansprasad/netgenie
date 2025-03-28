# app/routers/config_router.py

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Optional, Dict
from app.core.database import get_database
from app.core.auth import check_permission
from datetime import datetime
from app.schemas.user_schemas import UserResponse
from app.core.security import get_current_user
from fastapi.responses import PlainTextResponse
from app.models.config_model import Config 
from app.ai import ai_interface 
from app.models.devices_model import DeviceDetails
from app.models.config_template_model import ConfigTemplate
from app.models.config_values_model import ConfigValue
from app.models.config_model import ConfigUpdate
import logging

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)

@router.post(
    "/config",
    response_class=PlainTextResponse,
    status_code=200,
    name="config_to_template",
    dependencies=[Depends(check_permission)],
)
async def config_to_template(
    config: str = Body(
        ..., media_type="text/plain",
        title="Network Configuration",
        description="The network configuration to convert"),
    current_user: UserResponse = Depends(get_current_user),
    db = Depends(get_database)
) -> PlainTextResponse:
    """
    Endpoint to convert a network configuration to a Jinja2 template.
    Returns plain text Jinja2 template.
    """
    logger.info("Entering /config endpoint")
    logger.debug(f"Entering /config endpoint - User is Authenticated and Authorized")
    logger.debug(f"Received Configuration: {config}")
    prompt_file_path = "app/ai/prompts/config-2-j2.prompt"
    logger.debug(f"Using prompt file: {prompt_file_path}")

    try:
        logger.debug("Calling ai_interface.config_to_j2_n_json...")
        data_dict, result = ai_interface.config_to_j2_n_json(config, prompt_file_path)
        logger.debug(f"AI Service Result:\n{result}")

        # Check for error by looking for "error" in result
        if isinstance(result, str) and "error" in result.lower():
            logger.error(f"AI Service Error: {result}")
            raise HTTPException(status_code=500, detail=result)
        
        # Extract required values
        device_name = data_dict['device_name']
        jinja2_template = data_dict['Jinja2_Template']
        json_variables = data_dict['JSON_Variables']

        # Create template name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        template_name = f"{device_name}_{timestamp}"

        # Create ConfigTemplate object
        config_template = ConfigTemplate(
            template_name=template_name,
            username=current_user.username,  
            device_name=device_name,
            input_configuration=config,
            jinja2_template=jinja2_template,
            json_variables=json_variables
        )

        # Insert data into the database
        config_template_dict = config_template.model_dump()
        await db["config_templates"].insert_one(config_template_dict)
        logger.info(f"Template '{template_name}' saved to database.")

        logger.info("Successfully converted configuration to template.")
        return PlainTextResponse(result, media_type="text/plain")

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("Exiting /config endpoint")


@router.post("/configurations/", response_class=PlainTextResponse, status_code=201,
             dependencies=[Depends(check_permission)], name="create_configuration")
async def create_configuration(
    device_name: str = Query(..., description="Name of the device"),
    config_template_name: str = Query(..., description="Name of the configuration template"),
    config_values_name: str = Query(..., description="Name of the configuration values"),
    db = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Generates a configuration file using a Jinja2 template and JSON values,
    and stores it in the database, preventing duplicate entries based on configuration name.
    """
    logger.info("Entering /configurations/ (POST) endpoint")
    logger.debug(f"Device Name: {device_name}")
    logger.debug(f"Config Template Name: {config_template_name}")
    logger.debug(f"Config Values Name: {config_values_name}")

    # 1. Retrieve Device, Template and ConfigValues
    device = await db["devices"].find_one({"name": device_name})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    logger.debug(f"--Device found--\n{device}\n")

    template = await db["config_templates"].find_one({"template_name": config_template_name})
    if not template:
        raise HTTPException(status_code=404, detail="Config Template not found")
    logger.debug(f"--Template found--\n{template}\n")

    config_values = await db["config_values"].find_one({"name": config_values_name})
    if not config_values:
        raise HTTPException(status_code=404, detail="Config Values not found")
    logger.debug(f"--Config Values found--\n{config_values}\n")

    # 2. Generate Configuration
    try:
        # Extract data for LLM
        j2_template = template["jinja2_template"]
        json_data = config_values["config_data"]

        # Invoke LLM through ai_interface
        prompt_file_path = "app/ai/prompts/generate-configuration.prompt"
        result = ai_interface.generate_config_from_j2_json(j2_template, json_data, prompt_file_path)

        # Check for error in ai_interface result
        if isinstance(result, dict) and "error" in result:
            logger.error(f"LLM Generation Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
        config_data = result['message']

    except Exception as e:
        logger.exception(f"Error generating configuration: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating configuration: {e}")

    # 3. Create Configuration Document
    try:
        config_name = f"{device['customer_name']}_{device['type']}_{device['name']}_{device['location']}_cfg"
        config_name = config_name.replace(' ', '')
        logger.debug(f"Config name :{config_name}")

        # **CHECK FOR DUPLICATE CONFIGURATION NAME BEFORE INSERTION**
        existing_config = await db["configs"].find_one({"name": config_name})
        if existing_config:
            logger.warning(f"Configuration with name '{config_name}' already exists.  Skipping insertion.")
            raise HTTPException(status_code=409, detail=f"Configuration with name '{config_name}' already exists.") # Return 409 Conflict

        config = Config(
            name=config_name,
            device_name=device_name,
            config_data=config_data,
            created_by=current_user.username,
            created_at=datetime.now(),
            status="active"
        )
        config_dict = config.model_dump(exclude={"id"})
        result = await db["configs"].insert_one(config_dict)  # Insert into 'configs' collection
        new_config = await db["configs"].find_one({"_id": result.inserted_id})
        new_config["_id"] = str(new_config["_id"])
        new_config_obj = Config(**new_config)

    except HTTPException as he:  # Catch the HTTPException raised for duplicate config
        raise he
    except Exception as e:
        logger.exception(f"Error storing configuration: {e}")
        raise HTTPException(status_code=500, detail=f"Error storing configuration: {e}")

    # 4. Return Result

    response_text = f"** Configuration Name **\n{new_config_obj.name}\n\n** Configuration Data **\n{new_config_obj.config_data}"
    return PlainTextResponse(response_text, media_type="text/plain")


@router.get("/configurations/", response_model=List[Config],
            dependencies=[Depends(check_permission)], name="list_all_configs")
async def list_all_configs(db = Depends(get_database),current_user: UserResponse = Depends(get_current_user)):
    """Lists all configurations."""
    logger.info("Entering /configs/ (GET) endpoint - List all configs")
    configs = await db["configs"].find().to_list(length=None)
    for config in configs:
        config["_id"] = str(config["_id"])
    return configs

@router.get("/configurations/{name}", response_model=Config,
            dependencies=[Depends(check_permission)], name="read_config_by_name")
async def read_config_by_name(name: str, db = Depends(get_database),current_user: UserResponse = Depends(get_current_user)):
    """Retrieves a specific configuration by its name."""
    logger.info(f"Entering /configs/{{name}} (GET) endpoint - Read config by name: {name}")
    config = await db["configs"].find_one({"name": name})
    if config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    config["_id"] = str(config["_id"])
    return config

@router.get("/configurations/user/{username}", response_model=List[Config],
            dependencies=[Depends(check_permission)], name="list_configs_by_user")
async def list_configs_by_user(username: str, db = Depends(get_database),current_user: UserResponse = Depends(get_current_user)):
    """Lists configurations created by a specific user."""
    logger.info(f"Entering /configs/user/{{username}} (GET) endpoint - List configs by user: {username}")
    configs = await db["configs"].find({"created_by": username}).to_list(length=None)
    for config in configs:
        config["_id"] = str(config["_id"])
    return configs

@router.delete("/configurations/{name}",
             dependencies=[Depends(check_permission)], name="delete_config_by_name")
async def delete_config_by_name(name: str, db = Depends(get_database),current_user: UserResponse = Depends(get_current_user)):
    """Deletes a configuration by its name."""
    logger.info(f"Entering /configs/{{name}} (DELETE) endpoint - Delete config by name: {name}")
    result = await db["configs"].delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"message": "Configuration deleted successfully"}

@router.put("/configs/{name}", dependencies=[Depends(check_permission)], name="update_config_by_name")
async def update_config_by_name(
    name: str,
    new_name: str = Query(..., description="New name for the configuration"),
    config_update: ConfigUpdate = Body(None, description="The new configuration data (optional)"),
    db: dict = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)

):
    """Updates a configuration's data by its name."""
    logger.info(f"Entering /configs/{{name}} (PUT) endpoint - Update config by name: {name}")

    # Find the existing configuration
    existing_config = await db["configs"].find_one({"name": name})
    if existing_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")

    # Prepare the update data
    update_data = {}
    if config_update and config_update.config_data is not None:
        update_data["config_data"] = config_update.config_data

    update_data["name"] = new_name

    # Perform the update
    result = await db["configs"].update_one({"name": name}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")

    return {"message": "Configuration updated successfully"}