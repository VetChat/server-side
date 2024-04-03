from sqlalchemy.orm import Session
from ..models import QuestionSet, Symptom


class QuestionSetCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_question_set_id_by_id(self, question_set_id: int):
        return self.db.query(QuestionSet).filter(QuestionSet.question_set_id == question_set_id).first()
