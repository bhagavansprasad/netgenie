# app/schemas/config_template_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, Optional, Union
from datetime import datetime


class NetworkConfig(BaseModel):
    hostname: str
    interface_name: str
    ip_address: str
    subnet_mask: str
    description: Optional[str] = "Default Interface"

class ConfigToTemplateSuccessResponse(BaseModel):
    jinja2_template: str = Field(..., description="The generated Jinja2 template.")
    json_variables: Dict = Field(..., description="The extracted JSON variables.")


class ConfigToTemplateErrorResponse(BaseModel):
    error: str = Field(..., description="Error message if the conversion failed.")


class ConfigToTemplateResponse(BaseModel):
    # __root__: Union[ConfigToTemplateSuccessResponse, ConfigToTemplateErrorResponse]
    jinja2_template: Optional[str] = Field(None, description="The generated Jinja2 template.")
    json_variables: Optional[Dict] = Field(None, description="The extracted JSON variables.")
    error: Optional[str] = Field(None, description="Error message if the conversion failed.")

class ConfigTemplateListResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Template ID") # Changed type to str
    template_name: str = Field(..., description="Template Name")
    username: str = Field(..., description="Username")
    timestamp: datetime = Field(..., description="Timestamp")
    device_name: str = Field(..., description="Device Name")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True #this is important to get the alias working

class ConfigTemplateResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Template ID")
    template_name: str = Field(..., description="Template Name")
    username: str = Field(..., description="Username")
    timestamp: datetime = Field(..., description="Timestamp")
    device_name: str = Field(..., description="Device Name")
    input_configuration: str = Field(..., description="Input Configuration")
    jinja2_template: str = Field(..., description="Jinja2 Template")
    json_variables: Dict = Field(..., description="JSON Variables")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True #this is important to get the alias working
        
        
        
