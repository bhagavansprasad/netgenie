# app/ai/common.py
import logging
import json
import os
import re
import jinja2

from google.cloud import aiplatform
from vertexai.generative_models import (
    GenerativeModel,
    Content,
    Part
)
from jinja2 import Environment, FileSystemLoader

from app.core.settings import settings  # Import the settings


# Configure logging
logger = logging.getLogger(__name__)

class VertexAIConnector:  # Simple connector to get model object
    def __init__(self, model_name: str):
        self.model = GenerativeModel(model_name)


def parse_gentemplate_output(llm_output: str) -> list:
    """
    Parses the LLM output to extract the Jinja2 template and JSON variables.

    Args:
        llm_output: The raw text output from the LLM.

    Returns:
        A dictionary containing the extracted Jinja2 template and JSON variables,
        or an error message if parsing fails.
    """
    logger.debug(f"Entering _parse_llm_output")
    logger.debug(f"LLM Output: {llm_output}")

    template_match = re.search(r"```jinja2\n(.*?)\n```", llm_output, re.DOTALL)
    json_match = re.search(r"```json\n(.*?)\n```", llm_output, re.DOTALL)

    if not template_match or not json_match:
        error_message = "Could not find Jinja2 Template or JSON Variables sections in LLM's output."
        logger.error(error_message)
        return {"error": error_message}

    jinja2_template = template_match.group(1).strip()
    json_string = json_match.group(1).strip()

    try:
        json_variables = json.loads(json_string)
        # logger.debug(f"Extracted details: {json.dumps(json_variables, sort_keys=True, indent=4)}")  # Use json.dumps for pretty logging
        return {"jinja2_template": jinja2_template, "json_variables": json_variables}
    except json.JSONDecodeError as e:
        error_message = f"Error decoding JSON: {e}\nLLM Output: {llm_output}"
        logger.error(error_message)
    
    return {"error": error_message}

def parse_genconfig_output(llm_output: str) -> dict:
    """
    Parses the LLM output to extract the rendered Cisco IOS configuration,
    specifically removing generic code blocks delimited by ```.

    Args:
        llm_output: The raw text output from the LLM.

    Returns:
        A dictionary containing the rendered Cisco IOS configuration,
        or an error message if parsing fails.
    """
    logger.debug(f"Entering parse_genconfig_output")

    try:
        llm_output = llm_output.strip()
        llm_output = llm_output[3:-3].strip()
        
        return llm_output

    except Exception as e:
        error_message = f"Error processing LLM output: {e}"
        logger.error(error_message)
        return {"error": error_message}
    
    
def call_llm_chat(prompt_text: str) -> dict:
    """
    Sends a prompt to the Gemini model's chat interface and returns the response.

    Args:
        prompt_text: The text of the prompt to send to the chat model.

    Returns:
        A dictionary containing the extracted details, or an error message.
    """
    logger.debug(f"Entering call_llm_chat")

    try:
        aiplatform.init(project=settings.PROJECT_ID, location=settings.LOCATION)
        vertexai_connector = VertexAIConnector(settings.MODEL_NAME)
        chat = vertexai_connector.model.start_chat()

        contents = [Part.from_text(prompt_text)]

        response = chat.send_message(Content(role="user", parts=contents))

        llm_output = response.text.strip()

        llm_output = llm_output.strip()

        if not llm_output:
            error_message = "The LLM returned an empty response."
            logger.warning(error_message)
            return {"error": error_message}

        return llm_output
    
    except Exception as e:
        error_message = f"Error processing prompt: {e}"
        logger.exception(error_message)
        return {"error": error_message}
    finally:
        logger.debug(f"Exiting call_llm_chat")

def get_config_content(self, file_path: str) -> str:
    """
    Reads the content from file path and returns as string
    """
    logger.debug(f"Entering get_config_content")
    logger.debug(f"File Path: {file_path}")
    try:
        with open(file_path, "r") as f:
            content = f.read()
            logger.debug(f"File Content Loaded from {file_path}")
            return content
    except Exception as e:
        error_message = f"Value cannot be loaded from {file_path}: {e}"
        logger.error(error_message)
        return ""
    finally:
        logger.debug(f"Exiting get_config_content")

def _render_jinja2_template(j2_template: str, json_data: dict) -> str:
    """Renders a Jinja2 template with the provided JSON data."""
    logger.debug(f"Entering _render_jinja2_template")
    logger.debug(f"Jinja2 Template:\n{j2_template}")
    logger.debug(f"JSON Data:\n{json.dumps(json_data, indent=4)}")
    try:
        template = jinja2.Template(j2_template)
        rendered_config = template.render(json_data)  # Pass JSON data directly

        # Remove any leading or trailing whitespaces
        rendered_config_stripped = rendered_config.strip()
        logger.debug(f"Rendered Config (stripped):\n{rendered_config_stripped}")
        return rendered_config_stripped

    except jinja2.exceptions.TemplateError as e:
        error_message = f"Error rendering Jinja2 template: {e}"
        logger.error(error_message)
        raise ValueError(error_message)  # Re-raise as ValueError
    finally:
        logger.debug(f"Exiting _render_jinja2_template")
