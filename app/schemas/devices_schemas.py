from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DeviceDetails(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    customer_name: str = Field(..., description="Customer name")
    device_id: str = Field(..., description="Unique device ID")
    name: str = Field(..., description="Device name")
    type: str = Field(..., description="Device type (e.g., router, switch)")
    location: str = Field(..., description="Device location")
    status: str = Field(..., description="Device status (e.g., active, inactive)")
    created_by: str = Field(..., description="Username of the creator")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
