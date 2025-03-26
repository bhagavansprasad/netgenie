# app/schemas/config_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, Optional, Union


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
