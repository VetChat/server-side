from typing import List
from sqlalchemy.orm import Session
from ..models import TicketQuestion, TicketAnswerRecord, AnswerRecord, Answer, Question, QuestionSet, Symptom


class SummaryCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_ticket_info_by_ticket_ids(self, ticket_ids: List[int]):
        return self._fetch_ticket_info(TicketAnswerRecord.ticket_id.in_(ticket_ids))

    def fetch_summary_by_ticket_ids(self, ticket_ids: List[int]):
        return self._fetch_summary(AnswerRecord.ticket_id.in_(ticket_ids))

    def fetch_ticket_info_by_ticket_id(self, ticket_id: int):
        return self._fetch_ticket_info(TicketAnswerRecord.ticket_id == ticket_id)

    def fetch_ticket_questions_by_range(self, end_range: int):
        return (
            self.db.query(TicketQuestion.ticket_question,
                          TicketQuestion.ordinal)
            .filter(TicketQuestion.ordinal.in_(range(1, end_range + 1)))
            .order_by(TicketQuestion.ordinal)
            .all()
        )

    def fetch_summary_by_ticket_id(self, ticket_id: int):
        return self._fetch_summary(AnswerRecord.ticket_id == ticket_id)

    def _fetch_ticket_info(self, condition):
        return (
            self.db.query(TicketAnswerRecord)
            .filter(condition)
            .order_by(TicketAnswerRecord.ticket_id, TicketAnswerRecord.ordinal)
            .all()
        )

    def _fetch_summary(self, condition):
        return (
            self.db.query(AnswerRecord)
            .filter(condition)
            .order_by(AnswerRecord.symptom_id, AnswerRecord.ordinal)
            .all()
        )
