from typing import List

from pydantic import BaseModel


class QuestionSetRequest(BaseModel):
    questionSetIds: List[int]
