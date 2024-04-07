from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel
from .answer_schema import AnswerRead, AnswerCreate, AnswerCreateBulkResponse, AnswerUpdate, AnswerUpdateBulkResponse


class BaseQuestion(BaseModel):
    questionId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int


class QuestionId(BaseModel):
    questionId: int


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
    ordinal: int
    listAnswer: List[AnswerCreate]


class QuestionWithListAnswerCreateResponse(BaseQuestion):
    listAnswer: AnswerCreateBulkResponse
    message: str


class QuestionWithListAnswerUpdateResponse(BaseQuestion):
    listAnswer: AnswerUpdateBulkResponse
    message: str


class QuestionWithListAnswerUpdate(BaseQuestion):
    listAnswer: List[AnswerUpdate]


class QuestionWithListAnswerDeleteResponse(BaseQuestion):
    listAnswer: List[AnswerRead]
    message: str


class QuestionCreateFailedResponse(BaseModel):
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int
    message: str


class QuestionUpdateFailedResponse(BaseQuestion):
    message: str


class QuestionCreateBulkResponse(BaseModel):
    success: Optional[List[QuestionWithListAnswerCreateResponse]] = None
    failed: Optional[List[QuestionCreateFailedResponse]] = None


class QuestionUpdateBulkResponse(BaseModel):
    success: Optional[List[QuestionWithListAnswerUpdateResponse]] = None
    failed: Optional[List[QuestionUpdateFailedResponse]] = None


class QuestionDeleteBulkResponse(BaseModel):
    success: Optional[List[QuestionWithListAnswerDeleteResponse]] = None
    failed: Optional[List[QuestionUpdateFailedResponse]] = None
