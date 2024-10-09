from pydantic import BaseModel
from typing import List, Optional

class AnswerModel(BaseModel):
    answer_text: str
    related_field: str

class QuestionModel(BaseModel):
    question_text: str
    answers: List[AnswerModel]

class TestModel(BaseModel):
    title: str
    description: str
    questions: List[QuestionModel]
    created_by: str  # ID del creador (admin)
    created_at: Optional[str]
