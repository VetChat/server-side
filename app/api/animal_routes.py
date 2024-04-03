from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils import limiter
from ..database import get_db
from ..crud import AnimalCRUD
from ..schemas import AnimalRead, AnimalCreate, AnimalResponse, AnimalUpdate

router = APIRouter()


@router.get("/animals", response_model=List[AnimalRead], tags=["Animals"])
@limiter.limit("20/minute")
async def get_animal(request: Request, db: Session = Depends(get_db)) -> List[AnimalRead]:
    animal_crud = AnimalCRUD(db)
    animal_data = animal_crud.fetch_all_animal()
    animal_response = [
        AnimalRead(
            animalId=animal.animal_id,
            animalName=animal.animal_name
        )
        for animal in animal_data
    ]
    return animal_response


@router.get("/animal/{animal_id}", response_model=AnimalRead, tags=["Animals"])
@limiter.limit("5/minute")
async def get_animal_by_id(request: Request, animal_id: int, db: Session = Depends(get_db)) -> AnimalRead:
    animal_crud = AnimalCRUD(db)
    animal_data = animal_crud.fetch_animal_by_id(animal_id)
    if animal_data is None:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    return AnimalRead(
        animalId=animal_data.animal_id,
        animalName=animal_data.animal_name
    )


@router.post("/animal", response_model=AnimalResponse, tags=["Animals"])
@limiter.limit("10/minute")
async def add_animal(request: Request, animal: AnimalCreate, db: Session = Depends(get_db)) -> AnimalResponse:
    animal_crud = AnimalCRUD(db)
    existing_animal = animal_crud.fetch_animal_by_name(animal.animalName)
    if existing_animal:
        raise HTTPException(status_code=409, detail=f"Animal with name {animal.animalName} already exists")

    animal_data = animal_crud.add_animal(animal.animalName)

    return AnimalResponse(
        animalId=animal_data.animal_id,
        animalName=animal_data.animal_name,
        message="The animal has been successfully added."
    )


@router.put("/animal", response_model=AnimalUpdate, tags=["Animals"])
@limiter.limit("5/minute")
async def update_animal(request: Request, animal: AnimalRead,
                        db: Session = Depends(get_db)) -> AnimalUpdate:
    animal_crud = AnimalCRUD(db)
    existing_animal = animal_crud.fetch_animal_by_id(animal.animalId)
    if existing_animal is None:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal.animalId} not found")

    animal_data = animal_crud.update_animal(animal.animalId, animal.animalName)
    if animal_data is None:
        raise HTTPException(status_code=500, detail=f"Failed to update the animal id: {animal.animalId}")

    return AnimalUpdate(
        animalId=animal_data.animal_id,
        oldAnimalName=existing_animal.animal_name,
        newAnimalName=animal_data.animal_name,
        message="The animal has been successfully updated."
    )


@router.delete("/animal/{animal_id}", response_model=AnimalResponse, tags=["Animals"])
@limiter.limit("5/minute")
async def remove_animal(request: Request, animal_id: int, db: Session = Depends(get_db)) -> AnimalResponse:
    animal_crud = AnimalCRUD(db)
    animal_data = animal_crud.fetch_animal_by_id(animal_id)
    if animal_data is None:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    is_success = animal_crud.remove_animal(animal_id)
    if not is_success:
        raise HTTPException(status_code=500, detail=f"Failed to remove the animal id: {animal_id}")

    return AnimalResponse(
        animalId=animal_data.animal_id,
        animalName=animal_data.animal_name,
        message="The animal has been successfully removed."
    )
