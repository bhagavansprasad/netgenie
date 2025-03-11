from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Optional
from app.ai import ai_interface
from app.models.config_model import ConfigModel

import logging
# from app.models import ConfigModel

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)

@router.post("/config")
async def config_to_template(
    config: str = Body(..., media_type="text/plain"),
) -> dict:
    # logger.debug(f"Received Configuration:\n{config}")
    prompt_file_path = "app/ai/prompts/config-2-j2.prompt"  # Define the prompt file path

    try:
        result = ai_interface.config_to_j2_n_json(config, prompt_file_path)
        logger.debug(f"AI Service Result:\n{result}")

        # Check if the AI service returned an error
        if "error" in result:
            logger.error(f"AI Service Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        logger.debug(f"Jinja2 Template:\n{result.get('jinja2_template')}") # print the values
        logger.debug(f"JSON Variables:\n{result.get('json_variables')}") # print the values
        return result  # Return the result dictionary directly

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/generate_config")
# async def generate_config(
#     config_data: ConfigModel,
# ) -> dict:
@router.post("/generate_config")
async def generate_config(
    j2_template: str = Query(..., title="Jinja2 Template", description="Enter your Jinja2 template"),
    json_data: str = Query(..., title="JSON Data", description="Enter JSON values for the template")
) -> dict:
    """
    Generates a Cisco IOS configuration from a Jinja2 template and JSON variables.
    """
    j2_template = j2_template
    json_data = json_data
    logger.debug(f"Received Jinja2 Template:\n{j2_template}")
    logger.debug(f"Received JSON Data:\n{json_data}")


    prompt_file_path = "app/ai/prompts/j2-to-config.prompt"
    try:
        result = ai_interface.generate_config_from_j2_and_json(
            j2_template, json_data, prompt_file_path
        )
        logger.debug(f"AI Service Result:\n{result}")

        if "error" in result:
            logger.error(f"AI Service Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    