from pydantic import BaseModel


class QuestionSetRequest(BaseModel):
    questionSetId: int
