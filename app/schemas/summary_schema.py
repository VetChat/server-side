from typing import Optional, List

from pydantic import BaseModel


class AnswerSummary(BaseModel):
    answerRecordId: int
    question: str
    imagePath: Optional[str]
    ordinal: int
    answer: str
    summary: Optional[str]


class SymptomSummary(BaseModel):
    symptomId: int
    symptomName: str
    listAnswer: List[AnswerSummary]


class TicketInfo(BaseModel):
    ticketAnswerRecordId: int
    ticketQuestion: str
    ticketAnswer: str
    ordinal: int


class TicketLabel(BaseModel):
    ticketQuestion: str
    ordinal: int


class TicketSummaryResponse(BaseModel):
    ticketId: int
    label: List[TicketLabel]
    info: List[TicketInfo]
    summary: List[SymptomSummary]


class TicketEachSummaryResponse(BaseModel):
    ticketId: int
    info: List[TicketInfo]
    summary: List[SymptomSummary]
