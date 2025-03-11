# app/ai/ai-interface.py

import os
import logging
import json
import re
import jinja2

from app.ai import common  # Import the common functions
from app.core.settings import settings
from app.ai.common import get_config_content, _render_jinja2_template
from app.ai.common import parse_gentemplate_output
from app.ai.common import parse_genconfig_output

logger = logging.getLogger(__name__)

def config_to_j2_n_json(config: str, prompt_file_path: str = None) -> dict:
    """
    Generates a Jinja2 template and JSON variables from a network configuration
    using a prompt template and an LLM.

    Args:
        config: The network configuration string.
        prompt_file_path: The path to the prompt template file.

    Returns:
        A dictionary containing the Jinja2 template and JSON variables, or an error message.
    """
    logger.debug(f"Entering config_to_j2_n_json")
    logger.debug(f"Prompt File Path: {prompt_file_path}")

    try:
        prompt_file = prompt_file_path or settings.CONFIG_TO_J2_PROMPT

        with open(prompt_file, "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.format(network_config=config)

        llm_output = common.call_llm_chat(prompt)
        
        extracted_data = parse_gentemplate_output(llm_output)

        if "error" in extracted_data:
            logger.error(f"LLM Error: {extracted_data['error']}")
            return extracted_data

        return extracted_data

    except FileNotFoundError:
        error_message = f"Prompt file not found: {prompt_file_path}"
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logger.exception(error_message)
        return {"error": error_message}


def j2_and_json_to_config(j2_template: str, json_data: dict, prompt_file_path: str = None) -> dict:
    """
    Generates a Cisco IOS configuration from a Jinja2 template and JSON variables
    using a prompt template and an LLM. The template rendering is performed by the LLM.
    """
    logger.info(f"Entering j2_and_json_to_config")

    try:
        prompt_file = prompt_file_path or settings.J2_TO_CONFIG_PROMPT

        with open(prompt_file, "r") as f:
            prompt_template_string = f.read() # Read the prompt template as a string

        env = jinja2.Environment()
        prompt_template = env.from_string(prompt_template_string)
        prompt = prompt_template.render(j2_template=j2_template, json_data=json_data) # Use Jinja2 render

        llm_output = common.call_llm_chat(prompt)
        extracted_data = parse_genconfig_output(llm_output)

        if "error" in extracted_data:
            logger.error(f"LLM output Error: {extracted_data}")
            return extracted_data

        return {"message": extracted_data}

    except FileNotFoundError:
        error_message = f"Prompt file not found: {prompt_file_path}"
        logger.error(error_message)
        return {"error": error_message}

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logger.exception(error_message)
        return {"error": error_message}