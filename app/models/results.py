from pydantic import BaseModel
from typing import List, Optional

class ResponseModel(BaseModel):
    question_text: str
    selected_answer: str
    related_field: str

class ResultModel(BaseModel):
    user_id: str  # ID del estudiante
    test_id: str  # ID del test
    responses: List[ResponseModel]
    final_result: str
    created_at: Optional[str]
