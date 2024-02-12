from typing import List, Type, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import AnimalCRUD
from ..models import Animal
from ..schemas import AnimalRead

router = APIRouter()


@router.get("/animals", response_model=List[AnimalRead])
def fetch_animal(db: Session = Depends(get_db)) -> List[Type[Animal]]:
    animal_crud = AnimalCRUD(db)
    return animal_crud.fetch_all_animal()


@router.get("/animal/{animal_id}", response_model=AnimalRead)
def fetch_animal_by_id(animal_id: int, db: Session = Depends(get_db)) -> Optional[Animal]:
    animal_crud = AnimalCRUD(db)
    animal = animal_crud.fetch_animal_by_id(animal_id)
    if animal is None:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")
    return animal
