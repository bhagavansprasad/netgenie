# app/models/user_model.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

class User(BaseModel):
    id: str | None = None # Optional, MongoDB generates this
    username: str
    email: str
    roles: List[str]
    created_at: datetime | None = None
    updated_at: datetime | None = None

# app/models/customer_model.py
class Customer(BaseModel):
    id: str | None = None
    name: str
    description: str
    contact_email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

# app/models/template_model.py
class Template(BaseModel):
    id: str | None = None
    name: str
    description: str
    template_content: str
    is_global: bool
    customer_id: str | None = None # Only if not global
    created_at: datetime | None = None
    updated_at: datetime | None = None

# app/models/config_model.py
class CustomerConfig(BaseModel):
    id: str | None = None
    customer_id: str
    config_name: str
    config_data: dict  # Store the JSON config data
    created_at: datetime | None = None
    updated_at: datetime | None = None