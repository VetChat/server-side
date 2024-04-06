from typing import List, Optional
from pydantic import BaseModel
from .answer_schema import AnswerRead, AnswerCreate, AnswerBulkResponse, AnswerUpdate


class BaseQuestion(BaseModel):
    questionId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int


class QuestionWithListAnswer(BaseQuestion):
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


class QuestionWithListAnswerResponse(BaseQuestion):
    listAnswer: AnswerBulkResponse
    message: str


class QuestionWithListAnswerUpdate(BaseQuestion):
    listAnswer: List[AnswerUpdate]


class QuestionWithListAnswerDeleteResponse(BaseQuestion):
    listAnswer: List[AnswerRead]
    message: str


class QuestionFailedResponse(BaseModel):
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int
    message: str


class QuestionBulkResponse(BaseModel):
    success: Optional[List[QuestionWithListAnswerResponse]] = None
    failed: Optional[List[QuestionFailedResponse]] = None
