from typing import List

from pydantic import BaseModel


class QuestionSetRequest(BaseModel):
    question_set_ids: List[int]
