from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Customer(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    name: str = Field(..., description="Customer name (unique)")
    created_by: str = Field(..., description="Username of the creator")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
