from typing import Optional, List

from pydantic import BaseModel
from .answer_schema import AnswerRead, AnswerCreate


class QuestionWithListAnswer(BaseModel):
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
    listQuestion: List[QuestionWithListAnswer]

    class Config:
        from_attributes = True


class QuestionWintListAnswerCreate(BaseModel):
    questionSetId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int
    listAnswer: List[AnswerCreate]

    class Config:
        from_attributes = True
