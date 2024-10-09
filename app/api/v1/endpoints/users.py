from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserLogin, UserCreate, UserResponse
from app.core.security import verify_password, hash_password, create_access_token
from app.db.mongodb import user_collection
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()


# Ruta para registrar un nuevo usuario
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed_password = hash_password(user.password)

    new_user = {
        "email": user.email,
        "password_hash": hashed_password,
        "name": user.name,
        "role": "student",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    result = await user_collection.insert_one(new_user)
    created_user = await user_collection.find_one({"_id": result.inserted_id})

    return {
        "id": str(created_user["_id"]),
        "email": created_user["email"],
        "name": created_user["name"],
        "role": created_user["role"],
        "created_at": created_user["created_at"],
        "updated_at": created_user["updated_at"],
    }


# Ruta para iniciar sesión
@router.post("/login")
async def login(user_credentials: UserLogin):
    user = await user_collection.find_one({"email": user_credentials.email})
    if not user or not verify_password(
        user_credentials.password, user["password_hash"]
    ):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
