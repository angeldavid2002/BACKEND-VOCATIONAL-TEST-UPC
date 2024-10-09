from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Base para la información común de usuario
class UserBase(BaseModel):
    email: EmailStr
    name: str

# Esquema para crear un usuario (incluye la contraseña)
class UserCreate(UserBase):
    password: str

# Esquema para el inicio de sesión (login)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para devolver la respuesta al crear un usuario o al solicitar su información
class UserResponse(UserBase):
    id: str
    role: str  # 'student' o 'admin'
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cambiado desde orm_mode en Pydantic V2
