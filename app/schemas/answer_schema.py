from typing import Optional

from pydantic import BaseModel


class AnswerRead(BaseModel):
    answerId: int
    answer: str
    skipToQuestion: Optional[int] = None

    class Config:
        from_attributes = True
