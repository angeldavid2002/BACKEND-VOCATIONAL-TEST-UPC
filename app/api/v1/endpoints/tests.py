from fastapi import APIRouter, Depends, HTTPException
from app.schemas.test import TestCreate, TestResponse
from app.db.mongodb import test_collection
from bson.objectid import ObjectId
from datetime import datetime
from app.core.security import get_current_admin_user  # Importar la verificación de administrador

router = APIRouter()

# Ruta para crear un nuevo test (solo accesible para administradores)
@router.post("/create", response_model=TestResponse)
async def create_test(test: TestCreate, admin_user: dict = Depends(get_current_admin_user)):
    new_test = {
        "title": test.title,
        "description": test.description,
        "questions": test.questions,
        "created_by": admin_user["_id"],  # Asocia el test al administrador que lo creó
        "created_at": datetime.utcnow().isoformat(),
    }
    
    result = await test_collection.insert_one(new_test)
    created_test = await test_collection.find_one({"_id": result.inserted_id})
    
    return {
        "id": str(created_test["_id"]),
        "title": created_test["title"],
        "description": created_test["description"],
        "created_by": str(created_test["created_by"]),
        "created_at": created_test["created_at"]
    }

# Ejemplo de una ruta adicional para obtener todos los tests (sin protección)
@router.get("/", response_model=list[TestResponse])
async def get_tests():
    tests = await test_collection.find().to_list(1000)
    return [
        {
            "id": str(test["_id"]),
            "title": test["title"],
            "description": test["description"],
            "created_by": str(test["created_by"]),
            "created_at": test["created_at"]
        } for test in tests
    ]
