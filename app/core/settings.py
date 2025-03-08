# app/core/settings.py
import os

class Settings:
    PROJECT_ID = os.environ.get("PROJECT_ID")
    LOCATION = os.environ.get("LOCATION", "us-central1")  # Default to us-central1 if not set
    MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-1.5-pro-001")  # Default model
    PROMPT_FILE_PATH = "app/ai/prompts/config-2-j2.prompt"  # Default prompt file path
    CONFIG_TO_J2_PROMPT = "app/ai/prompts/config-2-j2.prompt"  # Default prompt file path

settings = Settings() # Create instance of the setting
