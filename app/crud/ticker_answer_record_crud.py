from typing import List

from sqlalchemy.orm import Session, joinedload
from ..models import TicketAnswerRecord, TicketQuestion


class TicketAnswerRecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_ticket_answer_records_by_ticket_id(self, ticket_id: int):
        return (self.db.query(TicketAnswerRecord)
                .options(joinedload(TicketAnswerRecord.ticket_question))
                .filter(TicketAnswerRecord.ticket_id == ticket_id)
                .all())

    def create_ticket_answer_record(self, ticket_id: int, question_id: int, answer: str):
        new_record = TicketAnswerRecord(
            ticket_id=ticket_id,
            ticket_question_id=question_id,
            ticket_answer=answer
        )
        self.db.add(new_record)
        self.db.commit()
