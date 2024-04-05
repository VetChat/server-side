from typing import List, Optional

from pydantic import BaseModel


class UrgentCaseRead(BaseModel):
    urgentId: int
    urgentName: str
    urgencyDetail: str
    duration: str

    class Config:
        from_attributes = True


class UrgentCaseWithUrgency(BaseModel):
    urgentId: int
    urgentName: str
    urgencyId: int
    urgencyDetail: str
    duration: str
    urgencyLevel: int


class UrgentCaseResponse(BaseModel):
    urgentId: int
    urgentName: str
    urgencyId: int
    animalId: int
    message: str

    class Config:
        from_attributes = True


class UrgentCaseCreate(BaseModel):
    urgentName: str
    urgencyId: int
    animalId: int

    class Config:
        from_attributes = True


class UrgentCaseUpdate(BaseModel):
    urgentId: int
    urgentName: str
    urgencyId: int
    message: str

    class Config:
        from_attributes = True


class UrgentCaseUpdateFailed(BaseModel):
    urgentId: int
    message: str


class UrgentCaseBulkResponse(BaseModel):
    success: Optional[List[UrgentCaseResponse]]
    failed: Optional[List[UrgentCaseUpdateFailed]]


class UrgentCaseId(BaseModel):
    urgentId: int

    class Config:
        from_attributes = True
