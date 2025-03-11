# app/ai/ai-interface.py

import os
import logging
import json
import re
import jinja2

from app.ai import common  # Import the common functions
from app.core.settings import settings
from app.ai.common import get_config_content, _render_jinja2_template

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

        # 1. Read the prompt template from the file
        with open(prompt_file, "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.format(network_config=config)

        # 3. Call the LLM API
        result = common.call_llm_chat(prompt) # call llm

        # Check if the AI service returned an error
        if "error" in result:
            logger.error(f"LLM Error: {result['error']}")
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


def generate_config_from_j2_and_json(j2_template: str, json_data: dict, prompt_file_path: str = None) -> dict:
    """
    Generates a Cisco IOS configuration from a Jinja2 template and JSON variables
    using a prompt template and an LLM. The template rendering is performed by the LLM.

    Args:
        j2_template: The Jinja2 template string.
        json_data: A dictionary containing the variables to render the template.
        prompt_file_path: The path to the prompt template file (optional).

    Returns:
        A dictionary containing the rendered Cisco IOS configuration, or an error message.
    """
    logger.debug(f"Entering generate_config_from_j2_and_json")
    logger.debug(f"Jinja2 Template:\n{j2_template}")
    logger.debug(f"JSON Data:\n{json.dumps(json_data, indent=4)}")
    logger.debug(f"Prompt File Path: {prompt_file_path}")  # Log prompt file path

    try:
        # 1. Determine the prompt file path
        prompt_file = prompt_file_path or settings.J2_TO_CONFIG_PROMPT
        logger.debug(f"Using prompt file: {prompt_file}")

        # 2. Read the prompt template from the file
        with open(prompt_file, "r") as f:
            prompt_template = f.read()
        logger.debug(f"Prompt Template:\n{prompt_template}")

        # 3. Construct the prompt for j2-to-config
        prompt = prompt_template.format(j2_template=j2_template, json_data=json.dumps(json_data))
        logger.debug(f"Generated Prompt:\n{prompt}")

        # 4. Call the LLM to generate the configuration
        result = common.call_llm_chat(prompt)

        # 5. Extract the rendered configuration
        if "error" in result:
            logger.error(f"LLM Error: {result['error']}")
            return result

        # 6. Basic parsing
        config_match = re.search(r"```cisco\n(.*?)\n```", result, re.DOTALL)

        if not config_match:
            error_message = f"Could not find Cisco IOS configuration section in LLM's output."  # Use f-string
            logger.error(error_message)
            return {"error": error_message}

        generated_config = config_match.group(1).strip()

        # Log results
        logger.debug(f"Returning Generated Config:\n{generated_config}")
        # 7. Return the rendered configuration
        return {"rendered_config": generated_config}

    except FileNotFoundError:
        error_message = f"Prompt file not found: {prompt_file_path}"
        logger.error(error_message)
        return {"error": error_message}

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logger.exception(error_message)
        return {"error": error_message}