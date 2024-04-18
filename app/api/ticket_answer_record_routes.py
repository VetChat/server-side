from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from app.utils import limiter
from app.database import get_db
from app.crud import TicketAnswerRecordCRUD
from app.schemas import TicketAnswerRecordUpdateResponse, TicketAnswerRecordUpdate


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(generate_unique_id_function=custom_generate_unique_id)


@router.put("/ticket_answer_record/update", response_model=TicketAnswerRecordUpdateResponse, tags=["Ticket Questions"])
@limiter.limit("10/minute")
async def update_pet_id(request: Request, ticket: TicketAnswerRecordUpdate,
                        db: Session = Depends(get_db)) -> TicketAnswerRecordUpdateResponse:
    ticket_question_crud = TicketAnswerRecordCRUD(db)
    question = ticket_question_crud.fetch_ticket_answer_record_by_id(ticket.ticketAnswerRecordId)
    if question is None:
        raise HTTPException(status_code=404,
                            detail=f"Ticket question with ticket id {ticket.ticketAnswerRecordId} not found")

    ticket_question_crud.update_ticket_answer_record(ticket.ticketAnswerRecordId, ticket.answer)

    return TicketAnswerRecordUpdateResponse(
        ticketAnswerRecordId=ticket.ticketAnswerRecordId,
        answer=ticket.answer,
        message="The ticket question pet id has been successfully updated."
    )
