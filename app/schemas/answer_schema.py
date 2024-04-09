from typing import Optional, List

from pydantic import BaseModel


class AnswerRead(BaseModel):
    answerId: int
    answer: str
    summary: str
    skipToQuestion: Optional[int] = None

    class Config:
        from_attributes = True


class AnswerCreate(BaseModel):
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


class AnswerResponse(BaseModel):
    answerId: int
    answer: str
    summary: Optional[str] = None
    skipToQuestion: Optional[int] = None
    message: str

    class Config:
        from_attributes = True


class AnswerCreateFailed(BaseModel):
    answer: str
    message: str


class AnswerUpdateFailed(AnswerUpdate):
    message: str


class AnswerCreateBulkResponse(BaseModel):
    success: Optional[List[AnswerResponse]] = None
    failed: Optional[List[AnswerCreateFailed]] = None


class AnswerUpdateBulkResponse(BaseModel):
    success: Optional[List[AnswerResponse]] = None
    failed: Optional[List[AnswerUpdateFailed]] = None
