from pydantic import BaseModel
from typing import List


class AnswerRecordCreate(BaseModel):
    ticket_id: int
    answer_ids: List[int]
