from pydantic import BaseModel


class SymptomRead(BaseModel):
    symptomId: int
    symptomName: str
