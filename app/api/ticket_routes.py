from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import TicketCreate, TicketId, TicketResponse
from ..crud import TicketCRUD, QuestionSetCRUD

router = APIRouter()


@router.post("/tickets", response_model=TicketId)
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)) -> TicketId:
    # Generate a ticket_id (this could be an auto-incremented ID in the database)
    ticket_crud = TicketCRUD(db)
    ticket = ticket_crud.create_ticket(ticket_data)

    if not ticket:
        raise HTTPException(status_code=500, detail="Failed to create a ticket")

    return TicketId(ticket_id=ticket.ticket_id)
    # # Get list of symptoms by animal_id
    # question_set_crud = QuestionSetCRUD(db)
    # symptoms = question_set_crud.get_symptoms_by_animal_id(ticket_data.animal_id)
    #
    # if not symptoms:
    #     raise HTTPException(status_code=404, detail="No symptoms found for the given animal ID")
    #
    # return symptoms
