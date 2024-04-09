from pydantic import BaseModel
from typing import List


class AnswerRecordId(BaseModel):
    questionId: int
    answer: str


class AnswerRecordCreate(BaseModel):
    ticketId: int
    listAnswer: List[AnswerRecordId]


class AnswerRecordResponse(BaseModel):
    ticketId: int
    message: str
