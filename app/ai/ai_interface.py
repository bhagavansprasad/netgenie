# app/ai/ai-interface.py

import os
import logging
import json

from app.ai import common  # Import the common functions
from app.core.settings import settings

logger = logging.getLogger(__name__)


def generate_j2_and_json_from_config(config: str, prompt_file_path: str = None) -> dict:
    """
    Generates a Jinja2 template and JSON variables from a network configuration
    using a prompt template and an LLM.

    Args:
        config: The network configuration string.
        prompt_file_path: The path to the prompt template file.

    Returns:
        A dictionary containing the Jinja2 template and JSON variables, or an error message.
    """
    logger.debug("Entering generate_j2_and_json_from_config")
    logger.debug("Prompt File Path: %s", prompt_file_path)

    try:
        prompt_file = prompt_file_path or settings.CONFIG_TO_J2_PROMPT

        # 1. Read the prompt template from the file
        with open(prompt_file, "r") as f:
            prompt_template = f.read()
        logger.debug("Prompt Template:\n%s", prompt_template)


        # 2. Combine the prompt template with the configuration
        prompt = prompt_template.format(network_config=config)
        
        # 3. Call the LLM API
        result = common.call_llm_chat(prompt) # call llm

        # Check if the AI service returned an error
        if "error" in result:
            logger.error("LLM Error: %s", result["error"])
            return result

        return result
    except FileNotFoundError:
        error_message = f"Prompt file not found: {prompt_file_path}"
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logger.exception(error_message)
        return {"error": error_message}
