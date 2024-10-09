from fastapi import APIRouter, Depends, HTTPException
from app.schemas import result as schemas
from app.db.mongodb import result_collection
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/submit", response_model=schemas.ResultModel)
async def submit_result(result: schemas.ResultModel):
    new_result = result.dict()
    new_result["created_at"] = datetime.utcnow().isoformat()
    await result_collection.insert_one(new_result)
    return new_result

@router.get("/analyze")
async def analyze_results():
    results = await result_collection.find().to_list(1000)
    if results:
        # Aquí puedes implementar lógica para analizar tendencias en los resultados
        return results
    raise HTTPException(status_code=404, detail="No results found")
