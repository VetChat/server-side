from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from app.utils import limiter
from app.database import get_db
from app.crud import AnswerRecordCRUD
from app.schemas import AnswerRecordCreate, AnswerRecordResponse


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(generate_unique_id_function=custom_generate_unique_id)


@router.post("/answer_records", response_model=AnswerRecordResponse, tags=["Answer_records"])
@limiter.limit("5/minute")
async def create_answer_records(
        request: Request, answer_record_data: AnswerRecordCreate, db: Session = Depends(get_db)
) -> AnswerRecordResponse:
    answer_record_crud = AnswerRecordCRUD(db)
    answer_data = [answer_record_crud.fetch_answer_data_by_question_id_and_answer(
        question_id=answer.questionId, answer=answer.answer
    ) for answer in answer_record_data.listAnswer]

    answer_record_crud.create_answer_records(
        ticket_id=answer_record_data.ticketId,
        answer_data=answer_data,
        answer_record_data=answer_record_data
    )
    return AnswerRecordResponse(
        ticketId=answer_record_data.ticketId,
        message="The answer record has been successfully created."
    )
