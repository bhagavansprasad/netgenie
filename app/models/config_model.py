# app/models/config_model.py
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class Config(BaseModel):
    """
    Represents a generated configuration in the database.
    """
    id: Optional[str] = Field(alias='_id', default=None)
    name: str = Field(..., description="Configuration name (unique)")
    device_name: str = Field(..., description="Device name (foreign key to devices collection)")
    config_data: str = Field(..., description="The configuration data")
    created_by: str = Field(..., description="Username of the creator")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    status: str = Field(default="active", description="Status of the configuration")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class ConfigUpdate(BaseModel):
    config_data: Optional[str] = None

