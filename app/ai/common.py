# app/ai/common.py
import logging
import json
import os
import re

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


def _parse_llm_output(llm_output: str) -> dict:
    """
    Parses the LLM output to extract the Jinja2 template and JSON variables.

    Args:
        llm_output: The raw text output from the LLM.

    Returns:
        A dictionary containing the extracted Jinja2 template and JSON variables,
        or an error message if parsing fails.
    """
    logger.debug("Entering _parse_llm_output")
    logger.debug("LLM Output: %s", llm_output)

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
        logger.debug(f"Extracted details: {json.dumps(json_variables, sort_keys=True, indent=4)}")  # Use json.dumps for pretty logging
        return {"jinja2_template": jinja2_template, "json_variables": json_variables}
    except json.JSONDecodeError as e:
        error_message = f"Error decoding JSON: {e}\nLLM Output: {llm_output}"
        logger.error(error_message)
        return {"error": error_message}
    finally:
        logger.debug("Exiting _parse_llm_output")
        
def call_llm_chat(prompt_text: str) -> dict:
    """
    Sends a prompt to the Gemini model's chat interface and returns the response.

    Args:
        prompt_text: The text of the prompt to send to the chat model.

    Returns:
        A dictionary containing the extracted details, or an error message.
    """
    logger.debug("Entering call_llm_chat")
    logger.debug(f"Prompt Text: {prompt_text}")

    try:
        # 1. Initialize Vertex AI
        aiplatform.init(project=settings.PROJECT_ID, location=settings.LOCATION)

        # 2.  Create VertexAI Connector
        vertexai_connector = VertexAIConnector(settings.MODEL_NAME)

        # 3. Initialize the chat session
        chat = vertexai_connector.model.start_chat()

        # 4. Prepare the message content
        contents = [
            Part.from_text(prompt_text)
        ]

        # 5. Send the message to the chat session
        response = chat.send_message(Content(role="user", parts=contents))

        # 6. Process the LLM Output
        llm_output = response.text.strip()

        if not llm_output:
            error_message = "The LLM returned an empty response."
            logger.warning(error_message)
            return {"error": error_message}

        # basic cleaning: Remove leading/trailing whitespaces
        # Note: You may need to add more sophisticated cleaning steps depending on the output of the LLM
        llm_output = llm_output.strip()

        logger.info(f"LLM Output: {llm_output}")

        if not llm_output:
            error_message = "The LLM returned an empty response."
            logger.warning(error_message)
            return {"error": error_message}

        llm_output = llm_output.strip()

        # 7. Parse the LLM output
        extracted_data = _parse_llm_output(llm_output) # parsing to a different module

        if "error" in extracted_data:
            return extracted_data  # Return the error directly

        logger.info(f"extracted_data: {extracted_data}")
        # 8. Construct returning results
        return extracted_data # construct results
    
    except Exception as e:
        error_message = f"Error processing prompt: {e}"
        logger.exception(error_message)
        return {"error": error_message}
    finally:
        logger.debug("Exiting call_llm_chat")
