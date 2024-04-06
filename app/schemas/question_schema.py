from typing import List, Optional
from pydantic import BaseModel
from .answer_schema import AnswerRead, AnswerCreate, AnswerBulkResponse


class QuestionWithListAnswer(BaseModel):
    questionId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int
    listAnswer: List[AnswerRead]


class QuestionResponse(BaseModel):
    symptomId: int
    symptomName: str
    listQuestion: List[QuestionWithListAnswer]


class QuestionWithListAnswerCreate(BaseModel):
    questionSetId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int
    listAnswer: List[AnswerCreate]


class QuestionWithListAnswerResponse(BaseModel):
    questionId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int
    listAnswer: AnswerBulkResponse
