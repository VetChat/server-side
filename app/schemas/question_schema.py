from typing import Optional, List

from pydantic import BaseModel
from .answer_schema import AnswerRead


class QuestionList(BaseModel):
    questionId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int
    listAnswer: List[AnswerRead]

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    symptomId: int
    symptomName: str
    listQuestion: List[QuestionList]

    class Config:
        from_attributes = True
