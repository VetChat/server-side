from pydantic import BaseModel


class AnimalRead(BaseModel):
    animalId: int
    name: str

    class Config:
        from_attributes = True


class AnimalCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class AnimalResponse(BaseModel):
    animalId: int
    name: str
    message: str
