from pydantic import BaseModel


class UrgencyRead(BaseModel):
    urgency_id: int
    urgency_detail: str
    duration: str
    urgency_level: int

    class Config:
        from_attributes = True


class UrgencyResponse(BaseModel):
    urgency_detail: str
    duration: str


class UrgencyId(BaseModel):
    urgency_id: int
