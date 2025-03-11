# /app/ai/models/config_model.py

from typing import Optional, Dict
from pydantic import BaseModel, Field

class ConfigModel(BaseModel): 
    j2_template: str = Field(
        ..., 
        title="Jinja2 Template",
        description="Enter your Jinja2 template here",
    )
    
    json_data: Dict = Field(
        ..., 
        title="JSON Data",
        description="Enter JSON values for the Jinja2 template",
    )
