from pydantic import BaseModel


class AnimalRead(BaseModel):
    animalId: int
    name: str

    class Config:
        from_attributes = True
