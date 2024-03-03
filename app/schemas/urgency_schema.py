from typing import List

from pydantic import BaseModel


class UrgencyRead(BaseModel):
    urgencyId: int
    urgencyDetail: str
    duration: str
    urgencyLevel: int

    class Config:
        from_attributes = True


class UrgencyResponse(BaseModel):
    urgencyDetail: str
    duration: str


class UrgencyIdRequest(BaseModel):
    urgencyId: List[int]
