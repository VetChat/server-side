from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils import limiter
from app.database import get_db
from app.crud import UrgentCaseCRUD, AnimalCRUD
from app.schemas import UrgentCaseByAnimalResponse, UrgentCaseResponse, UrgentCaseCreate, UrgentCaseUpdate, \
    UrgentCaseBulkResponse, UrgentCaseUpdateFailed

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


@router.get("/animal/{animal_id}/urgent_cases", response_model=List[UrgentCaseByAnimalResponse], tags=["Urgent Cases"])
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


@router.post("/animal/urgent_cases", response_model=List[UrgentCaseResponse], tags=["Urgent Cases"])
@limiter.limit("5/minute")
async def add_urgent_case(request: Request, urgent_case: UrgentCaseCreate,
                          db: Session = Depends(get_db)) -> UrgentCaseResponse:
    urgent_crud = UrgentCaseCRUD(db)
    existing_urgent_case = urgent_crud.fetch_urgent_case_by_name(urgent_case.animalId, urgent_case)
    if existing_urgent_case:
        raise HTTPException(status_code=409,
                            detail=f"Urgent case {urgent_case.urgentName} with {urgent_case.animalId} already exists")

    urgent_case_data = urgent_crud.add_urgent_case(urgent_case.urgentName, urgent_case.urgencyId)

    return UrgentCaseResponse(
        urgentId=urgent_case_data.urgent_id,
        urgentName=urgent_case_data.urgent_name,
        urgencyId=urgent_case_data.urgency_id,
        animal_id=urgent_case_data.animal_id,
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


@router.put("/urgent_cases/bulk", response_model=UrgentCaseBulkResponse, tags=["Urgent Cases"])
@limiter.limit("5/minute")
async def update_urgent_cases(request: Request, urgent_cases: List[UrgentCaseUpdate],
                              db: Session = Depends(get_db)) -> UrgentCaseBulkResponse:
    urgent_crud = UrgentCaseCRUD(db)
    existing_urgent_case = urgent_crud.fetch_urgent_case_by_ids([urgent_case.urgentId for urgent_case in urgent_cases])
    if len(existing_urgent_case) != len(urgent_cases):
        raise HTTPException(status_code=404, detail="One or more urgent cases not found")

    urgent_cases_data = UrgentCaseBulkResponse(success=[], failed=[])
    for urgent_case in urgent_cases:

        urgent_case_data = urgent_crud.update_urgent_case(urgent_case.urgentId, urgent_case.urgentName,
                                                          urgent_case.urgencyId)
        if urgent_case_data is not None:
            urgent_cases_data.success.append(
                UrgentCaseResponse(
                    urgentId=urgent_case_data.urgent_id,
                    urgentName=urgent_case_data.urgent_name,
                    urgencyId=urgent_case_data.urgency_id,
                    animalId=urgent_case_data.animal_id,
                    message="The urgent case has been successfully updated."
                )
            )
        else:
            urgent_cases_data.failed.append(
                UrgentCaseUpdateFailed(
                    urgentId=urgent_case.urgentId,
                    message="Failed to update the urgent case."
                )
            )

    return urgent_cases_data
