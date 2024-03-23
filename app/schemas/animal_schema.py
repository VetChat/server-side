from pydantic import BaseModel


class AnimalRead(BaseModel):
    animalId: int
    animalName: str

    class Config:
        from_attributes = True


class AnimalCreate(BaseModel):
    animalName: str

    class Config:
        from_attributes = True


class AnimalResponse(BaseModel):
    animalId: int
    animalName: str
    message: str


class AnimalUpdate(BaseModel):
    animalId: int
    oldAnimalName: str
    newAnimalName: str
    message: str

    class Config:
        from_attributes = True
