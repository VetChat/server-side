from typing import Optional

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    symptom_id: int
    symptom_name: str
    question_id: int
    question: str
    pattern: str
    image_path: Optional[str] = None
    ordinal: int

    class Config:
        from_attributes = True
