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


def parse_gentemplate_output(llm_output: str):
    """
    Parses the LLM output to extract the Jinja2 template and JSON variables.

    Args:
        llm_output: The raw text output from the LLM.

    Returns:
        A dictionary containing the extracted Jinja2 template and JSON variables,
        or an error message if parsing fails.
    """
    logger.info(f"Entering parse_gentemplate_output")
    logger.debug(f"LLM Output: {llm_output}")
    logger.info(f"Length of LLM Output: {len(llm_output) if llm_output else 0}")
    
    llm_output = llm_output.strip()
    llm_output = llm_output.strip('`')
    llm_output = llm_output.strip('json')
    llm_output = llm_output.strip()

    llm_outputd = json.loads(llm_output)

    logger.debug(f"LLM Output: {llm_outputd}")
    logger.debug(f"LLM Output: {type(llm_outputd)}")

    device_name = llm_outputd['device_name']
    jinja2_template = llm_outputd['Jinja2_Template']
    json_variables = llm_outputd['JSON_Variables']

    retval  = f"** device_name **\n{device_name}"
    retval += f"\n\n"
    
    retval += f"** Jinja2_Template **\n{jinja2_template}"
    retval += f"\n\n"
    
    retval += f"** json_variables **\n{json.dumps(json_variables, indent=4)}"
    retval += f"\n\n"
    
    logger.debug(f"Extracted device_name: {device_name}")
    logger.debug(f"Extracted jinja2_template: {jinja2_template}")
    logger.info(f"Length of extracted jinja2_template: {len(jinja2_template) if jinja2_template else 0}")
    logger.debug(f"Extracted json_variables: {json_variables}")
    
    logger.debug(f"retval :\n{retval}")

    return llm_outputd, retval

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
    logger.info(f"Entering parse_genconfig_output")
    logger.debug(f"LLM Output: {llm_output}")
    logger.info(f"Length of LLM Output: {len(llm_output) if llm_output else 0}")


    try:
        llm_output = llm_output.strip()
        llm_output = llm_output[3:-3].strip()

        logger.debug(f"Parsed LLM output: {llm_output}")
        logger.info(f"Length of Parsed LLM output: {len(llm_output) if llm_output else 0}")
        
        return llm_output

    except Exception as e:
        error_message = f"Error processing LLM output: {e}"
        logger.error(error_message)
        return {"error": error_message}
    finally:
        logger.info(f"Exiting parse_genconfig_output")
    
    
def call_llm_chat(prompt_text: str) -> dict:
    """
    Sends a prompt to the Gemini model's chat interface and returns the response.

    Args:
        prompt_text: The text of the prompt to send to the chat model.

    Returns:
        A dictionary containing the extracted details, or an error message.
    """
    logger.info(f"Entering call_llm_chat")
    logger.debug(f"Prompt Text: {prompt_text}")
    logger.info(f"Length of Prompt Text: {len(prompt_text) if prompt_text else 0}")

    try:
        aiplatform.init(project=settings.PROJECT_ID, location=settings.LOCATION)
        vertexai_connector = VertexAIConnector(settings.MODEL_NAME)
        chat = vertexai_connector.model.start_chat()

        contents = [Part.from_text(prompt_text)]

        response = chat.send_message(Content(role="user", parts=contents))

        llm_output = response.text.strip()

        llm_output = llm_output.strip()

        logger.debug(f"Raw LLM Output: {llm_output}")
        logger.info(f"Length of Raw LLM Output: {len(llm_output) if llm_output else 0}")

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
        logger.info(f"Exiting call_llm_chat")

def get_config_content(self, file_path: str) -> str:
    """
    Reads the content from file path and returns as string
    """
    logger.info(f"Entering get_config_content")
    logger.debug(f"File Path: {file_path}")

    try:
        with open(file_path, "r") as f:
            content = f.read()
            logger.debug(f"File Content Loaded from {file_path}")
            logger.info(f"Length of File Content Loaded: {len(content) if content else 0}")
            return content
    except Exception as e:
        error_message = f"Value cannot be loaded from {file_path}: {e}"
        logger.error(error_message)
        return ""
    finally:
        logger.info(f"Exiting get_config_content")

def _render_jinja2_template(j2_template: str, json_data: dict) -> str:
    """Renders a Jinja2 template with the provided JSON data."""
    logger.info(f"Entering _render_jinja2_template")
    logger.debug(f"Jinja2 Template:\n{j2_template}")
    logger.info(f"Length of Jinja2 Template: {len(j2_template) if j2_template else 0}")
    logger.debug(f"JSON Data:\n{json.dumps(json_data, indent=4)}")

    try:
        template = jinja2.Template(j2_template)
        rendered_config = template.render(json_data)  # Pass JSON data directly

        # Remove any leading or trailing whitespaces
        rendered_config_stripped = rendered_config.strip()
        logger.debug(f"Rendered Config (stripped):\n{rendered_config_stripped}")
        logger.info(f"Length of Rendered Config (stripped): {len(rendered_config_stripped) if rendered_config_stripped else 0}")
        return rendered_config_stripped

    except jinja2.exceptions.TemplateError as e:
        error_message = f"Error rendering Jinja2 template: {e}"
        logger.error(error_message)
        raise ValueError(error_message)  # Re-raise as ValueError
    finally:
        logger.info(f"Exiting _render_jinja2_template")