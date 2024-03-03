from pydantic import BaseModel


class UrgentCaseRead(BaseModel):
    urgentId: int
    urgentName: str
    urgencyDetail: str
    duration: str

    class Config:
        from_attributes = True


class UrgentCaseResponse(BaseModel):
    urgentId: int
    urgentName: str
    urgencyId: int
