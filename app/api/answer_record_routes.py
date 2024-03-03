from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import AnswerRecordCRUD
from ..schemas import AnswerRecordCreate, TicketSummaryResponse, SymptomSummary, AnswerSummary

router = APIRouter()


@router.post("/answer_records", response_model=TicketSummaryResponse)
def create_answer_records_and_return_summary(
        answer_record_data: AnswerRecordCreate, db: Session = Depends(get_db)
) -> TicketSummaryResponse:
    # Create answer records
    answer_record_crud = AnswerRecordCRUD(db)
    try:
        answer_record_crud.create_answer_records(
            ticket_id=answer_record_data.ticketId, answer_ids=[ar.answerId for ar in answer_record_data.listAnswer]
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
        # Create an instance of AnswerSummary with the details from answer_record
        list_answer = AnswerSummary(
            answerRecordId=answer_record.answer_record_id,
            questionId=answer_record.question_id,
            question=answer_record.question,
            ordinal=answer_record.ordinal,
            answer_id=answer_record.answer_id,
            answer=answer_record.answer,
            summary=answer_record.summary
        )

        # Find the existing symptom summary in the list or create a new one
        symptom_summary = next((s for s in summary if s.symptomId == answer_record.symptom_id), None)
        if not symptom_summary:
            # If a symptom summary does not exist, create a new one
            symptom_summary = SymptomSummary(
                symptomId=answer_record.symptom_id,
                symptomName=answer_record.symptom_name,
                listAnswer=[]  # Initialize an empty list for listAnswer
            )
            # Append the new symptom summary to the main summary list
            summary.append(symptom_summary)

        # Append the list_answer to the listAnswer list of the symptom_summary
        symptom_summary.listAnswer.append(list_answer)

    return TicketSummaryResponse(ticketId=answer_record_data.ticketId, summary=summary)
