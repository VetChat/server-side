from typing import List

from sqlalchemy.orm import Session, joinedload
from ..models import Question, Symptom, QuestionSet
from ..schemas import QuestionWithListAnswer


class QuestionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_question_by_question_id_and_question_set_id(self, question_id: int, question_set_id: int):
        return (
            self.db.query(Question)
            .filter(Question.question_id == question_id, Question.question_set_id == question_set_id)
            .first()
        )

    def fetch_question_by_question_ids_and_question_set_id(self, question_ids: List[int], question_set_id: int):
        return (
            self.db.query(Question)
            .filter(Question.question_id.in_(question_ids), Question.question_set_id == question_set_id)
            .all()
        )

    def fetch_questions_by_question_set_id(self, question_set_id: int):
        return (
            self.db.query(Question)
            .filter(Question.question_set_id == question_set_id)
            .options(joinedload(Question.answers))
            .order_by(Question.ordinal)
            .all()
        )

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

    def create_question(self, question_set_id: int, question: str, pattern: str, ordinal: int, image_path: str = None):
        new_question = Question(
            question_set_id=question_set_id,
            question=question,
            pattern=pattern,
            ordinal=ordinal,
            image_path=image_path
        )
        self.db.add(new_question)
        self.db.commit()
        self.db.refresh(new_question)
        return new_question
