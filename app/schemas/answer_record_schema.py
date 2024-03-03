from pydantic import BaseModel
from typing import List


class AnswerRecordCreate(BaseModel):
    ticketId: int
    answerIds: List[int]
