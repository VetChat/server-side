from pydantic import BaseModel


class UrgentCaseRead(BaseModel):
    urgent_id: int
    urgent_name: str
    urgency_detail: str
    duration: str

    class Config:
        from_attributes = True


class UrgentCaseResponse(BaseModel):
    urgent_id: int
    urgent_name: str
    urgency_id: int
    urgency_level: int
