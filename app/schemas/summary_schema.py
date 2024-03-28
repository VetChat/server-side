from typing import Optional, List

from pydantic import BaseModel


class AnswerSummary(BaseModel):
    answerRecordId: int
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


class TicketInfo(BaseModel):
    ticketAnswerRecordId: int
    ticketQuestionId: int
    ticketQuestion: str
    ticketAnswer: str
    pattern: str
    ordinal: int


class TicketSummaryResponse(BaseModel):
    ticketId: int
    info: List[TicketInfo]
    summary: List[SymptomSummary]
