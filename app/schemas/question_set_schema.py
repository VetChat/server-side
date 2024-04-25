from pydantic import BaseModel


class QuestionSetRequest(BaseModel):
    questionSetId: int


class QuestionSetCreateBody(BaseModel):
    symptomId: int
    animalId: int


class QuestionSetResponse(BaseModel):
    questionSetId: int
    symptomId: int
    animalId: int
    message: str


class QuestionSetRead(BaseModel):
    questionSetId: int
    symptomId: int
    symptomName: str
    animalId: int
    questionCount: int
