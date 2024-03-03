from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import UrgentCaseCRUD, AnimalCRUD
from ..schemas import UrgentCaseResponse

router = APIRouter()


@router.get("/urgent_cases/", response_model=List[UrgentCaseResponse])
def get_all_urgent_cases(db: Session = Depends(get_db)):
    urgent_crud = UrgentCaseCRUD(db)
    urgent_cases = urgent_crud.fetch_all_urgent_case()
    urgent_cases_response = [
        UrgentCaseResponse(
            urgentId=urgent.urgent_id,
            urgentName=urgent.urgent_name,
            urgencyId=urgent.urgency_id
        )
        for urgent in urgent_cases
    ]
    return urgent_cases_response


@router.get("/urgent_cases/animal/{animal_id}", response_model=List[UrgentCaseResponse])
def get_urgent_cases_by_animal_id(animal_id: int, db: Session = Depends(get_db)):
    animal_crud = AnimalCRUD(db)
    animal = animal_crud.fetch_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    urgent_crud = UrgentCaseCRUD(db)
    urgent_cases = urgent_crud.fetch_urgent_case_by_animal_id(animal_id)
    urgent_cases_response = [
        UrgentCaseResponse(
            urgentId=urgent.urgent_id,
            urgentName=urgent.urgent_name,
            urgencyId=urgent.urgency_id
        )
        for urgent in urgent_cases
    ]
    return urgent_cases_response
