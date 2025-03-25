from pydantic import BaseModel, constr
from typing import Optional

class RoleCreate(BaseModel):
    name: constr(min_length=3, max_length=50)  # Enforce name length
    description: str

class RoleResponse(BaseModel):
    id: str
    name: str
    description: str