# app/routers/ifaceconfig.py

from fastapi import APIRouter, Body, HTTPException, Query
from app.ai import ai_interface
from app.models.config_model import ConfigModel
from typing import Dict, List
import logging
from app.core.database import get_database

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
    logger.debug(f"Received Configuration: {config}") # Log input config
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
        if 'result' in result and 'config' in result:
            logger.info(f"Generated config length: {len(result['config'])}")
        return result

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("Exiting /generate_config endpoint")

@router.post("/generate_full_config")
async def generate_full_config(
    customer_name: str = Query(..., title="Customer Name", description="Name of the customer"),
    vrf_data: Dict = Body(..., title="VRF Data", description="JSON data for VRF configuration"),
    interface_data: Dict = Body(..., title="Interface Data", description="JSON data for interface configuration"),
    subinterface_data: Dict = Body(..., title="Subinterface Data", description="JSON data for subinterface configuration"),
    global_bgp_data: Dict = Body(..., title="Global BGP Data", description="JSON data for global BGP configuration"),
    local_bgp_data: Dict = Body(..., title="Local BGP Data", description="JSON data for local BGP configuration"),
) -> dict:
    """
    Endpoint to generate a complete Cisco IOS configuration from various JSON data inputs.
    Now customer_name will be passed as Query Parameter
    """
    logger.info("Entering /generate_full_config endpoint")
    logger.debug(f"Received customer_name: {customer_name}")
    logger.debug(f"Received vrf_data: {vrf_data}")
    logger.debug(f"Received interface_data: {interface_data}")
    logger.debug(f"Received subinterface_data: {subinterface_data}")
    logger.debug(f"Received global_bgp_data: {global_bgp_data}")
    logger.debug(f"Received local_bgp_data: {local_bgp_data}")

    try:
        result = ai_interface.generate_complete_config(
            customer_name=customer_name,
            vrf_data=vrf_data,
            interface_data=interface_data,
            subinterface_data=subinterface_data,
            global_bgp_data=global_bgp_data,
            local_bgp_data=local_bgp_data,
        )

        logger.debug(f"AI Service Result:\n{result}")

        if "error" in result:
            logger.error(f"AI Service Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        logger.info("Successfully generated full configuration.")
        if 'config' in result:
            logger.info(f"Generated full config length: {len(result['config'])}") # Log the total config length
        return result

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("Exiting /generate_full_config endpoint")


@router.get("/customers")
async def list_customers():
    db = get_database()
    customers = list(db["customers"].find())  # Get all customers as a list
    # Convert ObjectId to string for JSON serialization
    for customer in customers:
        customer["_id"] = str(customer["_id"])
    return customers