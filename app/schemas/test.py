from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    answer_text: str
    related_field: str  # 'ambiental', 'electronica', 'agroindustria', 'sistemas', 'no_ingenieria'

class Question(BaseModel):
    question_text: str
    answers: List[Answer]

# Esquema para crear un nuevo test
class TestCreate(BaseModel):
    title: str
    description: str
    questions: List[Question]

# Esquema para devolver el test en la respuesta
class TestResponse(BaseModel):
    id: str
    title: str
    description: str
    created_by: str  # ID del administrador que creó el test
    created_at: str

    class Config:
        from_attributes = True  # Para compatibilidad con Pydantic V2
