from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import UrgencyCRUD
from ..schemas import UrgencyResponse, UrgencyId

router = APIRouter()


@router.post("/urgency/most_urgent", response_model=UrgencyResponse)
def get_most_urgent_case(urgent_cases: List[UrgencyId], db: Session = Depends(get_db)) -> UrgencyResponse:
    urgency_crud = UrgencyCRUD(db)
    urgency_levels = urgency_crud.fetch_urgency_levels_by_ids([uc.urgency_id for uc in urgent_cases])

    if not urgency_levels:
        raise HTTPException(status_code=404, detail="No urgency records found for the provided IDs")

    # Find the most urgent case based on the lowest urgency_level
    most_urgent = min(urgency_levels, key=lambda urgency: urgency.urgency_level)
    return UrgencyResponse(urgency_detail=most_urgent.urgency_detail, duration=most_urgent.duration)
