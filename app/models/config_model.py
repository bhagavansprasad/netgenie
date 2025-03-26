# app/models/config_model.py
from pydantic import BaseModel, Field
from typing import Dict, Optional, Union

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

class ConfigToTemplateSuccessResponse(BaseModel):
    jinja2_template: str = Field(..., description="The generated Jinja2 template.")
    json_variables: Dict = Field(..., description="The extracted JSON variables.")


class ConfigToTemplateErrorResponse(BaseModel):
    error: str = Field(..., description="Error message if the conversion failed.")

class ConfigToTemplateResponse(BaseModel):
    retun_text: Optional[str] = Field(None, description="Text")
    error: Optional[str] = Field(None, description="Error message if the conversion failed.")

