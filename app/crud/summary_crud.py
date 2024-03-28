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

    def fetch_summary_by_ticket_id(self, ticket_id: int):
        return self._fetch_summary(AnswerRecord.ticket_id == ticket_id)

    def _fetch_ticket_info(self, condition):
        return (
            self.db.query(TicketAnswerRecord.ticket_answer_record_id,
                          TicketAnswerRecord.ticket_id,
                          TicketAnswerRecord.ticket_question_id,
                          TicketAnswerRecord.ticket_answer,
                          TicketQuestion.ticket_question,
                          TicketQuestion.pattern,
                          TicketQuestion.ordinal)
            .join(TicketAnswerRecord.ticket_question)
            .filter(condition)
            .order_by(TicketAnswerRecord.ticket_id, TicketQuestion.ordinal)
            .all()
        )

    def _fetch_summary(self, condition):
        return (
            self.db.query(AnswerRecord.answer_record_id,
                          AnswerRecord.ticket_id,
                          AnswerRecord.answer_id, Answer.question_id,
                          Answer.answer,
                          Answer.summary,
                          Answer.skip_to_question, Question.question,
                          Question.pattern,
                          Question.image_path,
                          Question.ordinal,
                          Symptom.symptom_id,
                          Symptom.symptom_name)
            .join(AnswerRecord.answers)
            .join(Answer.question)
            .join(Question.question_set)
            .join(QuestionSet.symptom)
            .filter(condition)
            .order_by(Symptom.symptom_id, Question.ordinal)
            .all()
        )
