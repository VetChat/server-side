from pydantic import BaseModel
from datetime import date


class TicketCreate(BaseModel):
    animal_id: int
    sex: str
    sterilize: str
    breed: str
    birth_when: date


class TicketResponse(BaseModel):
    symptom_id: int
    symptom_name: str
    question_set_id: int
