from typing import List, Union

from sqlalchemy.orm import Session, joinedload
from ..models import TicketAnswerRecord, TicketQuestion


class TicketAnswerRecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_ticket_answer_record_by_id(self, ticket_answer_record_id: int):
        return (self.db.query(TicketAnswerRecord)
                .filter(TicketAnswerRecord.ticket_answer_record_id == ticket_answer_record_id)
                .first())

    def fetch_ticket_answer_records_by_ticket_id(self, ticket_id: int):
        return (self.db.query(TicketAnswerRecord)
                .options(joinedload(TicketAnswerRecord.ticket_question))
                .filter(TicketAnswerRecord.ticket_id == ticket_id)
                .all())

    def create_ticket_answer_record(self, ticket_id: int, question: str, ordinal: int, answer: str,
                                    is_editable: bool = True):
        new_record = TicketAnswerRecord(
            ticket_id=ticket_id,
            ticket_question=question,
            ordinal=ordinal,
            ticket_answer=answer,
            is_editable=is_editable
        )
        self.db.add(new_record)
        self.db.commit()

    def update_ticket_answer_record(self, ticket_answer_record_id: int, answer: Union[str, int]):
        record = self.fetch_ticket_answer_record_by_id(ticket_answer_record_id)
        record.ticket_answer = answer
        self.db.commit()
