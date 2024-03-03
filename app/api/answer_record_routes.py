from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import AnswerRecordCRUD
from ..schemas import AnswerRecordCreate, TicketSummaryResponse

router = APIRouter()


@router.post("/answer_records", response_model=TicketSummaryResponse)
def create_answer_records_and_return_summary(
        answer_record_data: AnswerRecordCreate, db: Session = Depends(get_db)
) -> TicketSummaryResponse:
    # Create answer records
    answer_record_crud = AnswerRecordCRUD(db)
    try:
        answer_record_crud.create_answer_records(
            ticket_id=answer_record_data.ticketId, answer_ids=answer_record_data.answerIds
        )
    except HTTPException as e:
        # If an error is raised, return the error response
        raise e

    # Get the raw data of answers for the ticket
    answer_record_crud = AnswerRecordCRUD(db)
    answer_records = answer_record_crud.fetch_summary_by_ticket_id(answer_record_data.ticketId)

    if not answer_records:
        raise HTTPException(status_code=404, detail="No answers found for the given ticket ID")

    # Transform the raw data into the desired summary format
    summary = []
    for answer_record in answer_records:
        answer = answer_record.answers
        question = answer.question
        symptom = question.symptom

        # Find or create the symptom summary
        symptom_summary = next((s for s in summary if s['symptom_id'] == symptom.symptom_id), None)
        if not symptom_summary:
            symptom_summary = {
                'symptom_id': symptom.symptom_id,
                'symptom_name': symptom.symptom_name,
                'list_answer': []
            }
            summary.append(symptom_summary)

        # Append the answer to the symptom summary
        symptom_summary['list_answer'].append({
            'question_id': question.question_id,
            'question': question.question,
            'ordinal': question.ordinal,
            'answer_id': answer.answer_id,
            'answer': answer.answer,
            'summary': answer.summary
        })

    return TicketSummaryResponse(ticket_id=answer_record_data.ticketId, summary=summary)
