from sqlalchemy.orm import Session
from ..models import TicketAnswerRecord


class TicketAnswerRecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_ticket_answer_record(self, ticket_id: int, question_id: int, answer: str):
        new_record = TicketAnswerRecord(
            ticket_id=ticket_id,
            ticket_question_id=question_id,
            ticket_answer=answer
        )
        self.db.add(new_record)
        self.db.commit()
