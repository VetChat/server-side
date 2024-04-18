from typing import Optional, List
from datetime import datetime
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
    isEditable: bool = False


class TicketLabel(BaseModel):
    ticketQuestion: str
    ordinal: int


class TicketEachSummaryResponse(BaseModel):
    ticketId: int
    info: List[TicketInfo]
    summary: List[SymptomSummary]


class TicketDataResponse(BaseModel):
    ticketId: int
    info: List[TicketInfo]
    summary: List[SymptomSummary]
    recCreatedWhen: datetime


class TicketSummaryResponse(BaseModel):
    label: List[TicketLabel]
    listTicket: List[TicketDataResponse]
