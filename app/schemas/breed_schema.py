from pydantic import BaseModel


class BreedRead(BaseModel):
    breedId: int
    breedName: str


class BreedCreate(BaseModel):
    breedName: str
    animalId: int


class BreedUpdate(BaseModel):
    breedId: int
    breedName: str


class BreedCreateUpdateResponse(BaseModel):
    breedId: int
    breedName: str
    animalId: int
    message: str
