from sqlalchemy.orm import Session, joinedload
from ..models import TicketQuestion


class TicketQuestionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_ticket_questions_with_answers(self):
        questions = (
            self.db.query(TicketQuestion)
            .options(joinedload(TicketQuestion.ticket_answers))
            .order_by(TicketQuestion.ordinal)
            .all()
        )
        return questions
