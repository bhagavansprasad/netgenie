# app/core/settings.py
import os

class Settings:
    PROJECT_ID = os.environ.get("PROJECT_ID")
    LOCATION = os.environ.get("LOCATION", "us-central1")  # Default to us-central1 if not set
    MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-1.5-pro-001")  # Default model
    PROMPT_FILE_PATH = "app/ai/prompts/config-2-j2.prompt"  # Default prompt file path
    CONFIG_TO_J2_PROMPT = "app/ai/prompts/config-2-j2.prompt"  # Default prompt file path

    # MongoDB
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME", "admin")
    MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", "jnjnuh")  # Default password
    MONGODB_HOST = os.environ.get("MONGODB_HOST", "localhost") # Default host
    MONGODB_PORT = int(os.environ.get("MONGODB_PORT", 27017)) # Default port
    MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "netgenie_db")  # Default database name

    # JWT settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "Abcd!234")  # NEVER hardcode!
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60    
settings = Settings() # Create instance of the setting
