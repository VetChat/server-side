from typing import List

from sqlalchemy.orm import Session, joinedload
from ..models import Question, Symptom, QuestionSet


class QuestionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_questions_by_set_ids(self, question_set_ids: List[int]):
        return (
            self.db.query(Question, Symptom.symptom_id, Symptom.symptom_name)
            .join(Question.question_set)
            .join(QuestionSet.symptom)
            .filter(Question.question_set_id.in_(question_set_ids))
            .options(joinedload(Question.answers))
            .order_by(Symptom.symptom_id, Question.ordinal)
            .all()
        )
