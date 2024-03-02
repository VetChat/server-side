from typing import Optional

from pydantic import BaseModel


class AnswerRead(BaseModel):
    answer_id: int
    answer: str
    skip_to_question: Optional[int] = None

    class Config:
        from_attributes = True
