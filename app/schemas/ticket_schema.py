from pydantic import BaseModel
from datetime import date


class TicketCreate(BaseModel):
    animalId: int
    sex: str
    sterilize: str
    breed: str
    birthWhen: date


class TicketId(BaseModel):
    ticketId: int


class TicketResponse(BaseModel):
    symptomId: int
    symptomName: str
    questionSetId: int
