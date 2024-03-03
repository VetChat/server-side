from typing import Optional, List

from pydantic import BaseModel


class AnswerSummary(BaseModel):
    questionId: int
    question: str
    ordinal: int
    answer_id: int
    answer: str
    summary: Optional[str]


class SymptomSummary(BaseModel):
    symptomId: int
    symptomName: str
    listAnswer: List[AnswerSummary]


class TicketSummaryResponse(BaseModel):
    ticketId: int
    summary: List[SymptomSummary]
