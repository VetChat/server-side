from typing import List

from sqlalchemy.orm import Session
from ..models import Question, Symptom, QuestionSet


class QuestionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_questions_by_set_ids(self, question_set_ids: List[int]):
        return (
            self.db.query(Question, Symptom.symptom_id, Symptom.symptom_name)
            .join(QuestionSet, QuestionSet.question_set_id == Question.question_set_id)
            .join(Symptom, Symptom.symptom_id == QuestionSet.symptom_id)
            .filter(Question.question_set_id.in_(question_set_ids))
            .order_by(Symptom.symptom_id, Question.ordinal)
            .all()
        )
