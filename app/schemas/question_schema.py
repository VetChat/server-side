from typing import Optional, List

from pydantic import BaseModel
from .answer_schema import AnswerRead


class QuestionResponse(BaseModel):
    symptom_id: int
    symptom_name: str
    question_id: int
    question: str
    pattern: str
    image_path: Optional[str] = None
    ordinal: int
    list_answer: List[AnswerRead]

    class Config:
        from_attributes = True
