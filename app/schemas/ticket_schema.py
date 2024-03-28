from typing import List

from pydantic import BaseModel
from datetime import date


class TicketAnswer(BaseModel):
    questionId: int
    answer: str


class TicketCreate(BaseModel):
    animalId: int
    listAnswer: List[TicketAnswer]


class TicketId(BaseModel):
    ticketId: int
