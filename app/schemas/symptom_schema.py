from pydantic import BaseModel


class SymptomRead(BaseModel):
    symptomId: int
    symptomName: str


class SymptomCreateBody(BaseModel):
    symptomName: str


class SymptomCreateResponse(BaseModel):
    symptomId: int
    symptomName: str
    message: str
