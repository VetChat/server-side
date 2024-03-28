from pydantic import BaseModel


class SymptomRead(BaseModel):
    symptomId: int
    symptomName: str


class SymptomCreateBody(BaseModel):
    symptomName: str


class SymptomResponse(BaseModel):
    symptomId: int
    symptomName: str
    message: str


class SymptomUpdate(BaseModel):
    symptomId: int
    oldSymptomName: str
    newSymptomName: str
    message: str

    class Config:
        from_attributes = True


class SymptomWithQuestions(BaseModel):
    symptomId: int
    symptomName: str
    questionSetId: int
