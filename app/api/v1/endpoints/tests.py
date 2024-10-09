from fastapi import APIRouter, Depends
from app.schemas.test import TestCreate, TestResponse
from app.db.mongodb import test_collection
from datetime import datetime
from app.core.security import get_current_user

router = APIRouter()

# Ruta para crear un nuevo test (solo para usuarios autenticados)
@router.post("/create", response_model=TestResponse)
async def create_test(test: TestCreate, current_user: dict = Depends(get_current_user)):
    new_test = {
        "title": test.title,
        "description": test.description,
        "questions": test.questions,
        "created_by": current_user["_id"],
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
