from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils import limiter
from ..database import get_db
from ..schemas import TicketCreate, TicketId
from ..crud import TicketCRUD, TicketAnswerRecordCRUD

router = APIRouter()


@router.post("/tickets", response_model=TicketId, tags=["Tickets"])
@limiter.limit("5/minute")
async def create_ticket(request: Request, ticket_data: TicketCreate, db: Session = Depends(get_db)) -> TicketId:
    # Generate a ticket_id (this could be an auto-incremented ID in the database)
    ticket_crud = TicketCRUD(db)
    ticket = ticket_crud.create_ticket(ticket_data)

    if not ticket:
        raise HTTPException(status_code=500, detail="Failed to create a ticket")

    # Store the list of answers in ticket_answer_record for this ticket_id
    ticket_answer_record_crud = TicketAnswerRecordCRUD(db)
    for answer_data in ticket_data.listAnswer:
        ticket_answer_record_crud.create_ticket_answer_record(
            ticket_id=ticket.ticket_id,
            question_id=answer_data.questionId,
            answer=answer_data.answer
        )

    return TicketId(ticketId=ticket.ticket_id)
