from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils import limiter
from ..database import get_db
from ..crud import AnimalCRUD
from ..schemas import AnimalRead, AnimalCreate, AnimalRemoveResponse

router = APIRouter()


@router.get("/animals", response_model=List[AnimalRead], tags=["Animals"])
@limiter.limit("20/minute")
async def get_animal(request: Request, db: Session = Depends(get_db)) -> List[AnimalRead]:
    animal_crud = AnimalCRUD(db)
    animal_data = animal_crud.fetch_all_animal()
    animal_response = [
        AnimalRead(
            animalId=animal.animal_id,
            name=animal.name
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
        name=animal_data.name
    )


@router.post("/animal", response_model=AnimalRead, tags=["Animals"])
@limiter.limit("10/minute")
async def add_animal(request: Request, animal: AnimalCreate, db: Session = Depends(get_db)) -> AnimalRead:
    animal_crud = AnimalCRUD(db)
    existing_animal = animal_crud.fetch_animal_by_name(animal.name)
    if existing_animal:
        raise HTTPException(status_code=409, detail=f"Animal with name {animal.name} already exists")

    animal_data = animal_crud.add_animal(animal.name)

    return AnimalRead(
        animalId=animal_data.animal_id,
        name=animal_data.name
    )


@router.delete("/animal/{animal_id}", response_model=AnimalRemoveResponse, tags=["Animals"])
@limiter.limit("5/minute")
async def remove_animal_id(request: Request, animal_id: int, db: Session = Depends(get_db)) -> AnimalRemoveResponse:
    animal_crud = AnimalCRUD(db)
    animal_data = animal_crud.fetch_animal_by_id(animal_id)
    if animal_data is None:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    animal_crud.remove_animal(animal_id)

    print(f"print na {animal_data}")
    return AnimalRemoveResponse(
        animalId=animal_data.animal_id,
        name=animal_data.name,
        message="The animal has been successfully removed."
    )
