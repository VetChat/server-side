from typing import List, Type, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import AnimalCRUD
from ..models import Animal
from ..schemas import AnimalRead

router = APIRouter()


@router.get("/animals", response_model=List[AnimalRead])
def fetch_animal(db: Session = Depends(get_db)) -> List[AnimalRead]:
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


@router.get("/animal/{animal_id}", response_model=AnimalRead)
def fetch_animal_by_id(animal_id: int, db: Session = Depends(get_db)) -> AnimalRead:
    animal_crud = AnimalCRUD(db)
    animal_data = animal_crud.fetch_animal_by_id(animal_id)
    if animal_data is None:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    return AnimalRead(
        animalId=animal_data.animal_id,
        name=animal_data.name
    )