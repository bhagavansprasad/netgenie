# app/schemas/config_schema.py
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class Config(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    name: str = Field(..., description="Configuration name (unique)")
    customer: str = Field(..., description="Customer name (must exist in customers collection)")
    config_data: Dict = Field(..., description="JSON object containing the configuration data")
    created_by: str = Field(..., description="Username of the creator")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    status: Optional[str] = Field(default="active", description="Status of the configuration")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ConfigListResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    customer: str
    config_data: Dict  
    created_by: str
    created_at: datetime
    status: str
    
class ConfigResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    customer: str
    config_data: Dict
    created_by: str
    created_at: datetime
    status: str
