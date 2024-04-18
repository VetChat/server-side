from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from .answer_schema import AnswerRead, AnswerCreateUpdateDelete, AnswerCreateUpdateDeleteBulkResponse


class BaseQuestion(BaseModel):
    questionId: int
    question: str
    pattern: str
    imagePath: Optional[str] = None
    ordinal: int


class QuestionId(BaseModel):
    questionId: int


class QuestionWithListAnswer(BaseQuestion):
    listAnswer: Optional[List[AnswerRead]] = None


class QuestionResponse(BaseModel):
    symptomId: int
    symptomName: str
    listQuestion: List[QuestionWithListAnswer]


class QuestionWithListAnswerCreate(BaseModel):
    questionSetId: int
    question: str
    pattern: str
    ordinal: int
    imagePath: Optional[HttpUrl] = None
    haveImage: bool
    listAnswer: Optional[AnswerCreateUpdateDelete] = None


class QuestionWithListAnswerResponse(BaseQuestion):
    listAnswer: Optional[AnswerCreateUpdateDeleteBulkResponse] = None
    message: str


class QuestionWithListAnswerUpdate(BaseQuestion):
    haveImage: bool
    listAnswer: Optional[AnswerCreateUpdateDelete] = None


class QuestionWithListAnswerCreateUpdate(BaseModel):
    questionId: Optional[int] = None
    questionSetId: int
    question: str
    pattern: str
    ordinal: int
    imagePath: Optional[HttpUrl] = None
    haveImage: bool
    listAnswer: Optional[AnswerCreateUpdateDelete] = None


class QuestionDeleteResponse(BaseModel):
    questionId: int
    message: str


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


class QuestionCreateUpdateDelete(BaseModel):
    createUpdate: List[QuestionWithListAnswerCreateUpdate]
    delete: Optional[List[QuestionId]] = None


class QuestionCreateUpdateDeleteSuccessResponse(BaseModel):
    create: Optional[List[QuestionWithListAnswerResponse]] = None
    update: Optional[List[QuestionWithListAnswerResponse]] = None
    delete: Optional[List[QuestionWithListAnswerDeleteResponse]] = None


class QuestionCreateUpdateDeleteFailedResponse(BaseModel):
    create: Optional[List[QuestionCreateFailedResponse]] = None
    update: Optional[List[QuestionUpdateFailedResponse]] = None
    delete: Optional[List[QuestionDeleteResponse]] = None


class QuestionCreateUpdateDeleteBulkResponse(BaseModel):
    success: Optional[QuestionCreateUpdateDeleteSuccessResponse] = None
    failed: Optional[QuestionCreateUpdateDeleteFailedResponse] = None
