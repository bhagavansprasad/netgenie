from fastapi import APIRouter, Body, HTTPException
from app.ai import ai_interface

import logging
# from app.models import ConfigModel

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)

@router.post("/config")
async def config_to_template(
    config: str = Body(..., media_type="text/plain"),
    summary: str = "Configuration to Jinja Template",
) -> dict:
    # logger.debug(f"Received Configuration:\n{config}")
    prompt_file_path = "app/ai/prompts/config-2-j2.prompt"  # Define the prompt file path

    try:
        result = ai_interface.generate_j2_and_json_from_config(config, prompt_file_path)
        logger.debug(f"AI Service Result:\n{result}")

        # Check if the AI service returned an error
        if "error" in result:
            logger.error(f"AI Service Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        print("Jinja2 Template:\n", result.get("jinja2_template")) # print the values
        print("JSON Variables:\n", result.get("json_variables")) # print the values
        return result  # Return the result dictionary directly

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
