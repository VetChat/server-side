from typing import Optional, List

from pydantic import BaseModel


class AnswerRead(BaseModel):
    answerId: int
    answer: str
    summary: Optional[str] = None
    skipToQuestion: Optional[int] = None

    class Config:
        from_attributes = True


class AnswerUpdate(BaseModel):
    answerId: int
    answer: str
    summary: Optional[str] = None
    skipToQuestion: Optional[int] = None

    class Config:
        from_attributes = True


class AnswerCreateUpdate(BaseModel):
    answerId: Optional[int] = None
    answer: str
    summary: Optional[str] = None
    skipToQuestion: Optional[int] = None


class AnswerDelete(BaseModel):
    answerId: int


class AnswerCreateUpdateDelete(BaseModel):
    createUpdate: List[AnswerCreateUpdate]
    delete: Optional[List[AnswerDelete]]


class AnswerResponse(BaseModel):
    answerId: int
    answer: str
    summary: Optional[str] = None
    skipToQuestion: Optional[int] = None
    message: str


class AnswerCreateFailed(BaseModel):
    answer: str
    message: str


class AnswerUpdateFailed(AnswerUpdate):
    message: str


class AnswerDeleteResponse(BaseModel):
    answerId: int
    message: str


class AnswerCreateUpdateDeleteSuccessResponse(BaseModel):
    create: Optional[List[AnswerResponse]] = None
    update: Optional[List[AnswerResponse]] = None
    delete: Optional[List[AnswerDeleteResponse]] = None


class AnswerCreateUpdateDeleteFailedResponse(BaseModel):
    create: Optional[List[AnswerCreateFailed]] = None
    update: Optional[List[AnswerUpdateFailed]] = None
    delete: Optional[List[AnswerDeleteResponse]] = None


class AnswerCreateUpdateDeleteBulkResponse(BaseModel):
    success: Optional[AnswerCreateUpdateDeleteSuccessResponse] = None
    failed: Optional[AnswerCreateUpdateDeleteFailedResponse] = None
