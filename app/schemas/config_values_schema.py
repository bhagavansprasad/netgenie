# app/schemas/config_values_schema.py
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class ConfigValue(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    name: str = Field(..., description="Configuration name (unique)")
    device_name: str = Field(..., description="Device name (foreign key to devices collection)")
    config_data: Dict = Field(..., description="JSON object containing the configuration data")
    created_by: str = Field(..., description="Username of the creator")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    status: Optional[str] = Field(default="active", description="Status of the configuration")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ConfigValueListResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    device_name: str
    config_data: Dict  
    created_by: str
    created_at: datetime
    status: str
    
class ConfigValueResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    device_name: str
    config_data: Dict
    created_by: str
    created_at: datetime
    status: str
