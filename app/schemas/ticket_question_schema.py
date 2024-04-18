from pydantic import BaseModel
from typing import List, Optional, Union


class TicketAnswerRead(BaseModel):
    answerId: int
    answer: str


class TicketQuestionRead(BaseModel):
    questionId: int
    question: str
    pattern: str
    ordinal: int
    isRequired: bool
    listAnswer: Optional[List[TicketAnswerRead]]
