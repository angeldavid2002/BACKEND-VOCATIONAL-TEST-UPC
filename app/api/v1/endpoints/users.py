from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserLogin, UserCreate, UserResponse  # Importar los esquemas necesarios
from app.core.security import verify_password, hash_password, create_access_token  # Importar funciones de seguridad
from app.db.mongodb import user_collection  # Conexión a la base de datos MongoDB
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()

# Ruta para registrar usuarios
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    # Verificar si el correo ya está registrado
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    # Cifrar la contraseña
    hashed_password = hash_password(user.password)
    
    # Crear un nuevo usuario
    new_user = {
        "email": user.email,
        "password_hash": hashed_password,
        "name": user.name,
        "role": "student",  # El rol por defecto es estudiante
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    # Insertar el usuario en la base de datos
    result = await user_collection.insert_one(new_user)
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    
    # Retornar el usuario creado
    return {
        "id": str(created_user["_id"]),
        "email": created_user["email"],
        "name": created_user["name"],
        "role": created_user["role"],
        "created_at": created_user["created_at"],
        "updated_at": created_user["updated_at"]
    }

# Ruta para el inicio de sesión
@router.post("/login")
async def login(user_credentials: UserLogin):
    # Buscar al usuario por correo
    user = await user_collection.find_one({"email": user_credentials.email})
    if not user:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    # Verificar la contraseña
    if not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    # Crear un token JWT
    token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})
    
    # Retornar el token de acceso
    return {"access_token": token, "token_type": "bearer"}
