from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int
    email: EmailStr

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role_id: int
    email: str

class AuthResponse(BaseModel):
    username: str
    email: EmailStr
    access_token: str
    token_type: str
    role: Dict[str, int | str]  
