from pydantic import BaseModel


class AnimalRead(BaseModel):
    animal_id: int
    name: str

    class Config:
        orm_mode = True
