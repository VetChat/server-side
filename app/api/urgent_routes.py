from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import UrgentCRUD, AnimalCRUD
from ..schemas import UrgentRead

router = APIRouter()


@router.get("/urgent_cases/", response_model=List[UrgentRead])
def get_urgent_cases(db: Session = Depends(get_db)):
    urgent_crud = UrgentCRUD(db)
    urgent_cases = urgent_crud.fetch_all_urgent_case()
    return urgent_cases


@router.get("/urgent_cases/animal/{animal_id}", response_model=List[UrgentRead])
def get_urgent_cases_by_animal(animal_id: int, db: Session = Depends(get_db)):
    animal_crud = AnimalCRUD(db)
    animal = animal_crud.fetch_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    urgent_crud = UrgentCRUD(db)
    urgent_cases = urgent_crud.fetch_urgent_case_by_animal_id(animal_id)
    return urgent_cases
