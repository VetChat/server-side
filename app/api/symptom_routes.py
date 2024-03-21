from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils import limiter
from ..database import get_db
from ..schemas import TicketResponse
from ..crud import QuestionSetCRUD, AnimalCRUD

router = APIRouter()


@router.get("/symptoms/animal/{animal_id}", response_model=List[TicketResponse], tags=["Symptoms"])
@limiter.limit("10/minute")
async def get_symptoms_by_animal_id(request: Request, animal_id: int, db: Session = Depends(get_db)) -> (
        List)[TicketResponse]:
    # Retrieve the ticket to get the animal_id
    animal_crud = AnimalCRUD(db)
    animal = animal_crud.fetch_animal_by_id(animal_id)

    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Get list of symptoms by animal_id
    question_set_crud = QuestionSetCRUD(db)
    symptoms_data = question_set_crud.fetch_symptoms_by_animal_id(animal.animal_id)
    symptoms_response: List[TicketResponse] = [
        TicketResponse(
            symptomId=symptoms.symptom_id,
            symptomName=symptoms.symptom_name,
            questionSetId=symptoms.question_set_id
        )
        for symptoms in symptoms_data
    ]

    return symptoms_response
