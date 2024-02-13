from pydantic import BaseModel


class SymptomRead(BaseModel):
    symptom_id: int
    symptom_name: str
