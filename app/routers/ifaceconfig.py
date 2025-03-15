# app/routers/ifaceconfig.py

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
    """
    Endpoint to convert a network configuration to a Jinja2 template and JSON variables.
    """
    logger.info("Entering /config endpoint")
    logger.debug(f"Received Configuration:\n{config}")
    prompt_file_path = "app/ai/prompts/config-2-j2.prompt"  # Define the prompt file path
    logger.debug(f"Using prompt file: {prompt_file_path}")

    try:
        result = ai_interface.config_to_j2_n_json(config, prompt_file_path)
        logger.debug(f"AI Service Result:\n{result}")

        # Check if the AI service returned an error
        if "error" in result:
            logger.error(f"AI Service Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        logger.debug(f"Jinja2 Template:\n{result.get('jinja2_template')}") # print the values
        logger.debug(f"JSON Variables:\n{result.get('json_variables')}") # print the values
        logger.info("Successfully converted configuration to template.")
        return result  # Return the result dictionary directly

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("Exiting /config endpoint")

# @router.post("/generate_config")
# async def template_to_config(
#     j2_template: str = Query(..., title="Jinja2 Template", description="Enter your Jinja2 template"),
#     json_data: str = Query(..., title="JSON Data", description="Enter JSON values for the template")
# ) -> dict:
@router.post("/generate_config")
async def template_to_config(
    config_data: ConfigModel = Body(..., title="Configuration Data", description="Jinja2 template and JSON data")
) -> dict:
    """
    Endpoint to generate a Cisco IOS configuration from a Jinja2 template and JSON variables.
    """
    logger.info("Entering /generate_config endpoint")
    logger.debug(f"Received config_data:\n{config_data}")  # Log the entire config_data object

    j2_template = config_data.j2_template
    json_data = config_data.json_data
    logger.debug(f"Extracted j2_template:\n{j2_template}")
    logger.debug(f"Extracted json_data:\n{json_data}")

    prompt_file_path = "app/ai/prompts/j2-to-config.prompt"
    logger.debug(f"Using prompt file: {prompt_file_path}")
    
    try:
        result = ai_interface.j2_and_json_to_config(
            j2_template, json_data, prompt_file_path
        )
        logger.debug(f"AI Service Result:\n{result}")


        if "error" in result:
            logger.error(f"AI Service Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        logger.info("Successfully generated configuration from template.")
        return result

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("Exiting /generate_config endpoint")