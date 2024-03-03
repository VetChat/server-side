from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import AnswerRecordCRUD
from ..schemas import AnswerRecordCreate, AnswerRecordResponse

router = APIRouter()


@router.post("/answer_records", response_model=AnswerRecordResponse)
def create_answer_records_and_return_summary(
        answer_record_data: AnswerRecordCreate, db: Session = Depends(get_db)
) -> AnswerRecordResponse:
    # Create answer records
    answer_record_crud = AnswerRecordCRUD(db)
    answer_record_crud.create_answer_records(
        ticket_id=answer_record_data.ticketId,
        answer_ids=[ar.answerId for ar in answer_record_data.listAnswer]
    )

    return AnswerRecordResponse(
        ticketId=answer_record_data.ticketId,
        message="The answer record has been successfully created."
    )
