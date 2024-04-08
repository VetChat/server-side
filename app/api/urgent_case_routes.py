from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from app.utils import limiter
from app.database import get_db
from app.crud import UrgentCaseCRUD, AnimalCRUD
from app.schemas import UrgentCaseWithUrgency, UrgentCaseResponse, UrgentCaseCreate, UrgentCaseUpdate


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(generate_unique_id_function=custom_generate_unique_id)


@router.get("/urgent_cases/", response_model=List[UrgentCaseWithUrgency], tags=["Urgent Cases"])
@limiter.limit("10/minute")
async def get_all_urgent_cases(request: Request, db: Session = Depends(get_db)) -> List[UrgentCaseWithUrgency]:
    urgent_crud = UrgentCaseCRUD(db)
    urgent_cases = urgent_crud.fetch_all_urgent_case()
    urgent_cases_response = [
        UrgentCaseWithUrgency(
            urgentId=urgent.urgent_id,
            urgentName=urgent.urgent_name,
            urgencyId=urgent.urgency_id,
            urgencyDetail=urgent.urgency_detail,
            duration=urgent.duration,
            urgencyLevel=urgent.urgency_level
        )
        for urgent in urgent_cases
    ]
    return urgent_cases_response


@router.get("/animal/{animal_id}/urgent_cases", response_model=List[UrgentCaseWithUrgency], tags=["Urgent Cases"])
@limiter.limit("10/minute")
async def get_urgent_cases_by_animal_id(request: Request, animal_id: int, db: Session = Depends(get_db)) -> (
        List)[UrgentCaseWithUrgency]:
    animal_crud = AnimalCRUD(db)
    animal = animal_crud.fetch_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    urgent_crud = UrgentCaseCRUD(db)
    urgent_cases = urgent_crud.fetch_urgent_case_by_animal_id(animal_id)
    urgent_cases_response = [
        UrgentCaseWithUrgency(
            urgentId=urgent.urgent_id,
            urgentName=urgent.urgent_name,
            urgencyId=urgent.urgency_id,
            urgencyDetail=urgent.urgency_detail,
            duration=urgent.duration,
            urgencyLevel=urgent.urgency_level
        )
        for urgent in urgent_cases
    ]
    return urgent_cases_response


@router.post("/animal/urgent_cases", response_model=UrgentCaseResponse, tags=["Urgent Cases"])
@limiter.limit("5/minute")
async def add_urgent_case(request: Request, urgent_case: UrgentCaseCreate,
                          db: Session = Depends(get_db)) -> UrgentCaseResponse:
    urgent_crud = UrgentCaseCRUD(db)
    existing_urgent_case = urgent_crud.fetch_urgent_case_by_name(urgent_case.animalId, urgent_case.urgentName)
    if existing_urgent_case:
        raise HTTPException(status_code=409,
                            detail=f"Urgent case {urgent_case.urgentName} in animal id {urgent_case.animalId} already "
                                   f"exists")

    urgent_case_data = urgent_crud.add_urgent_case(urgent_case.urgentName, urgent_case.urgencyId, urgent_case.animalId)

    return UrgentCaseResponse(
        urgentId=urgent_case_data.urgent_id,
        urgentName=urgent_case_data.urgent_name,
        urgencyId=urgent_case_data.urgency_id,
        animalId=urgent_case_data.animal_id,
        message="The urgent case has been successfully added."
    )


@router.put("/urgent_cases", response_model=UrgentCaseResponse, tags=["Urgent Cases"])
@limiter.limit("5/minute")
async def update_urgent_case(request: Request, urgent_case: UrgentCaseUpdate,
                             db: Session = Depends(get_db)) -> UrgentCaseResponse:
    urgent_crud = UrgentCaseCRUD(db)
    existing_urgent_case = urgent_crud.fetch_urgent_case_by_id(urgent_case.urgentId)
    if existing_urgent_case is None:
        raise HTTPException(status_code=404, detail=f"Urgent case with id {urgent_case.urgent_id} not found")

    urgent_case_data = urgent_crud.update_urgent_case(urgent_case.urgentId, urgent_case.urgentName,
                                                      urgent_case.urgencyId)

    if urgent_case_data is None:
        raise HTTPException(status_code=500, detail=f"Failed to update urgent case id: {urgent_case.urgentId}")

    return UrgentCaseResponse(
        urgentId=urgent_case_data.urgent_id,
        urgentName=urgent_case_data.urgent_name,
        urgencyId=urgent_case_data.urgency_id,
        animalId=urgent_case_data.animal_id,
        message="The urgent case has been successfully updated."
    )


@router.delete("/urgent_cases/{urgent_id}", response_model=UrgentCaseResponse, tags=["Urgent Cases"])
@limiter.limit("5/minute")
async def remove_urgent_case(request: Request, urgent_id: int, db: Session = Depends(get_db)) -> UrgentCaseResponse:
    urgent_crud = UrgentCaseCRUD(db)
    urgent_case_data = urgent_crud.fetch_urgent_case_by_id(urgent_id)
    if urgent_case_data is None:
        raise HTTPException(status_code=404, detail=f"Urgent case with id {urgent_id} not found")

    is_success = urgent_crud.remove_urgent_case(urgent_id)
    if not is_success:
        raise HTTPException(status_code=500, detail=f"Failed to remove the urgent case id: {urgent_id}")

    return UrgentCaseResponse(
        urgentId=urgent_case_data.urgent_id,
        urgentName=urgent_case_data.urgent_name,
        urgencyId=urgent_case_data.urgency_id,
        animalId=urgent_case_data.animal_id,
        message="The urgent case has been successfully removed."
    )
