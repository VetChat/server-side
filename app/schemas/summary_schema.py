from typing import Optional, List

from pydantic import BaseModel


class AnswerSummary(BaseModel):
    question_id: int
    question: str
    ordinal: int
    answer_id: int
    answer: str
    summary: Optional[str]


class SymptomSummary(BaseModel):
    symptom_id: int
    symptom_name: str
    list_answer: List[AnswerSummary]


class TicketSummaryResponse(BaseModel):
    ticket_id: int
    summary: List[SymptomSummary]
