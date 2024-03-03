from pydantic import BaseModel
from typing import List


class AnswerRecordId(BaseModel):
    answerId: int


class AnswerRecordCreate(BaseModel):
    ticketId: int
    listAnswer: List[AnswerRecordId]


class AnswerRecordResponse(BaseModel):
    ticketId: int
    message: str
