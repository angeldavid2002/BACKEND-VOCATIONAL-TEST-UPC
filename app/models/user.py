from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class UserModel(BaseModel):
    email: EmailStr
    password_hash: str
    name: str
    role: str  # 'student' o 'admin'
    created_at: Optional[str]
    updated_at: Optional[str]

class UserCreateModel(BaseModel):
    email: EmailStr
    password: str
    name: str
