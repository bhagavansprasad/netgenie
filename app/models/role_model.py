from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Role(BaseModel):
    id: str | None = None
    name: str
    description: str
