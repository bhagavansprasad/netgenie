from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Role(BaseModel):
    id: Optional[str] = None  # MongoDB's ObjectId as string
    name: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
