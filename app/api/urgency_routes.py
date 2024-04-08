from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from app.utils import limiter
from app.database import get_db
from app.crud import UrgencyCRUD
from app.schemas import UrgencyResponse, UrgencyMostRequest, UrgencyRead


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(generate_unique_id_function=custom_generate_unique_id)


@router.get("/urgency", response_model=List[UrgencyRead], tags=["Urgency"])
@limiter.limit("30/minute")
async def get_all_urgency(request: Request, db: Session = Depends(get_db)) -> List[UrgencyRead]:
    urgency_crud = UrgencyCRUD(db)
    urgencies = urgency_crud.fetch_all_urgency()

    response = [
        UrgencyRead(
            urgencyId=urgency.urgency_id,
            urgencyDetail=urgency.urgency_detail,
            duration=urgency.duration,
            urgencyLevel=urgency.urgency_level
        )
        for urgency in urgencies
    ]
    return response


@router.post("/urgency/most_urgent", response_model=UrgencyResponse, tags=["Urgency"])
@limiter.limit("10/minute")
async def get_most_urgent_case(request: Request, urgent_cases: List[UrgencyMostRequest],
                               db: Session = Depends(get_db)) -> UrgencyResponse:
    urgency_crud = UrgencyCRUD(db)
    urgency_levels = urgency_crud.fetch_urgency_levels_by_ids([uc.urgencyId for uc in urgent_cases])

    if not urgency_levels:
        raise HTTPException(status_code=404, detail="No urgency records found for the provided IDs")

    # Find the most urgent case based on the lowest urgency_level
    most_urgent = min(urgency_levels, key=lambda urgency: urgency.urgency_level)
    return UrgencyResponse(urgencyDetail=most_urgent.urgency_detail, duration=most_urgent.duration)
