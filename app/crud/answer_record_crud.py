from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from ..models import AnswerRecord, Answer, Question, Symptom, QuestionSet


class AnswerRecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_answer_records(self, ticket_id: int, answer_ids: List[int]):
        try:
            # Create answer records
            for answer_id in answer_ids:
                answer_record = AnswerRecord(ticket_id=ticket_id, answer_id=answer_id)
                self.db.add(answer_record)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()  # Roll back the transaction on error
            raise HTTPException(status_code=400, detail="Invalid ticket ID or answer ID")

    def fetch_summary_by_ticket_id(self, ticket_id: int):
        # Retrieve the summary of answers for the ticket
        return (
            self.db.query(AnswerRecord.answer_id, AnswerRecord.answer_record_id, Answer.question_id, Answer.answer,
                          Answer.summary, Symptom.symptom_id, Symptom.symptom_name, Question.question, Question.ordinal)
            .join(AnswerRecord.answers)
            .join(Answer.question)
            .join(Question.question_set)
            .join(QuestionSet.symptom)
            .filter(AnswerRecord.ticket_id == ticket_id)
            .order_by(Symptom.symptom_id, Question.ordinal)
            .all()
        )
