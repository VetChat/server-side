from pydantic import BaseModel


class UrgentRead(BaseModel):
    urgent_id: int
    urgent_name: str
    urgency_detail: str
    duration: str

    class Config:
        from_attributes = True
