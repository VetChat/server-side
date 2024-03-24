from typing import Type, List, Optional
from sqlalchemy.orm import Session, joinedload
from ..models import Ticket, TicketQuestion, TicketAnswerRecord, AnswerRecord, Answer, Question, QuestionSet, Symptom
from ..schemas import AnimalCreate


class SummaryCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_ticket_info_by_ticket_ids(self, ticket_ids: List[int]):
        return (self.db.query(TicketAnswerRecord.ticket_answer_record_id,
                              TicketAnswerRecord.ticket_id,
                              TicketAnswerRecord.ticket_question_id,
                              TicketAnswerRecord.ticket_answer,
                              TicketQuestion.ticket_question,
                              TicketQuestion.pattern,
                              TicketQuestion.ordinal)
                .join(TicketAnswerRecord.ticket_question)
                .filter(TicketAnswerRecord.ticket_id.in_(ticket_ids))
                .order_by(TicketAnswerRecord.ticket_id, TicketQuestion.ordinal)
                .all())

    def fetch_summary_by_ticket_ids(self, ticket_ids: List[int]):
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
            .filter(AnswerRecord.ticket_id.in_(ticket_ids))
            .order_by(Symptom.symptom_id, Question.ordinal)
            .all()
        )

    def fetch_summary(self):
        result = (self.db.query(Ticket)
                  .options(joinedload(Ticket.ticket_answer_records))
                  .options(joinedload(Ticket.answer_records))
                  .options(joinedload(TicketAnswerRecord.ticket_question))
                  .options(joinedload(AnswerRecord.answers))
                  .options(joinedload(AnswerRecord.answers))
                  .options(joinedload(Question.question_set))
                  .options(joinedload(QuestionSet.symptom))
                  .all())
        return result
