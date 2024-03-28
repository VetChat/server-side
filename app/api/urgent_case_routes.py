from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils import limiter
from app.database import get_db
from app.crud import UrgentCaseCRUD, AnimalCRUD
from app.schemas import UrgentCaseByAnimalResponse, UrgentCaseResponse

router = APIRouter()


@router.get("/urgent_cases/", response_model=List[UrgentCaseByAnimalResponse], tags=["Urgent Cases"])
@limiter.limit("10/minute")
async def get_all_urgent_cases(request: Request, db: Session = Depends(get_db)) -> List[UrgentCaseByAnimalResponse]:
    urgent_crud = UrgentCaseCRUD(db)
    urgent_cases = urgent_crud.fetch_all_urgent_case()
    urgent_cases_response = [
        UrgentCaseByAnimalResponse(
            urgentId=urgent.urgent_id,
            urgentName=urgent.urgent_name,
            urgencyId=urgent.urgency_id
        )
        for urgent in urgent_cases
    ]
    return urgent_cases_response


@router.get("/urgent_cases/animal/{animal_id}", response_model=List[UrgentCaseByAnimalResponse], tags=["Urgent Cases"])
@limiter.limit("10/minute")
async def get_urgent_cases_by_animal_id(request: Request, animal_id: int, db: Session = Depends(get_db)) -> (
        List)[UrgentCaseByAnimalResponse]:
    animal_crud = AnimalCRUD(db)
    animal = animal_crud.fetch_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    urgent_crud = UrgentCaseCRUD(db)
    urgent_cases = urgent_crud.fetch_urgent_case_by_animal_id(animal_id)
    urgent_cases_response = [
        UrgentCaseByAnimalResponse(
            urgentId=urgent.urgent_id,
            urgentName=urgent.urgent_name,
            urgencyId=urgent.urgency_id
        )
        for urgent in urgent_cases
    ]
    return urgent_cases_response


@router.post("animals/{animal_id}/urgent_cases", response_model=List[UrgentCaseResponse], tags=["Urgent Cases"])
@limiter.limit("5/minute")
async def add_urgent_case(request: Request, animal_id: int, urgent_case: UrgentCaseByAnimalResponse,
                          db: Session = Depends(get_db)) -> UrgentCaseResponse:
    urgent_crud = UrgentCaseCRUD(db)
    existing_urgent_case = urgent_crud.fetch_urgent_case_by_name(animal_id, urgent_case.urgentName)
    if existing_urgent_case:
        raise HTTPException(status_code=409, detail=f"Urgent case with name {urgent_case.urgentName} already exists")

    urgent_case_data = urgent_crud.add_urgent_case(urgent_case.urgentName, urgent_case.urgencyId)

    return UrgentCaseResponse(
        urgentId=urgent_case_data.urgent_id,
        urgentName=urgent_case_data.urgent_name,
        urgencyId=urgent_case_data.urgency_id,
        animal_id=urgent_case_data.animal_id,
        message="The urgent case has been successfully added."
    )
