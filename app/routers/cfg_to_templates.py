from fastapi import APIRouter, Body, HTTPException, Depends, Query
from fastapi.responses import PlainTextResponse
from app.ai import ai_interface
from typing import Dict, List, Union
import logging
from app.core.database import get_database
from app.core.auth import check_permission
from app.models.config_model import ConfigToTemplateResponse
from app.models.config_model import ConfigToTemplateSuccessResponse
from app.models.config_model import ConfigToTemplateErrorResponse

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
        result = ai_interface.config_to_j2_n_json(config, prompt_file_path)
        logger.debug(f"AI Service Result:\n{result}")

        # Check for error by looking for "error" in result
        if isinstance(result, str) and "error" in result.lower():
            logger.error(f"AI Service Error: {result}")
            raise HTTPException(status_code=500, detail=result)

        logger.info("Successfully converted configuration to template.")
        return PlainTextResponse(result, media_type="text/plain")

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("Exiting /config endpoint")
