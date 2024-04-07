from sqlalchemy.orm import Session, joinedload
from ..models import QuestionSet, Symptom, Question


class QuestionSetCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_question_set_id_by_id(self, question_set_id: int):
        return self.db.query(QuestionSet).filter(QuestionSet.question_set_id == question_set_id).first()

    def fetch_question_set_by_symptom_animal_id(self, symptom_id: int, animal_id: int):
        return (self.db.query(QuestionSet)
                .filter(QuestionSet.symptom_id == symptom_id,
                        QuestionSet.animal_id == animal_id)
                .first())

    def fetch_question_set_info_by_id(self, question_set_id: int):
        return (self.db.query(QuestionSet)
                .filter(QuestionSet.question_set_id == question_set_id)
                .options(joinedload(QuestionSet.symptom), joinedload(QuestionSet.animal))
                .first())

    def fetch_question_set_info_by_question_id(self, question_id: int):
        return (self.db.query(QuestionSet)
                .join(QuestionSet.questions)
                .filter(Question.question_id == question_id)
                .options(joinedload(QuestionSet.symptom), joinedload(QuestionSet.animal))
                .first())

    def create_question_set(self, symptom_id: int, animal_id: int):
        new_question_set = QuestionSet(
            symptom_id=symptom_id,
            animal_id=animal_id
        )
        self.db.add(new_question_set)
        self.db.commit()
        self.db.refresh(new_question_set)
        return new_question_set

    def remove_question_set(self, question_set_id: int):
        question_set = self.fetch_question_set_id_by_id(question_set_id)
        if question_set:
            self.db.delete(question_set)
            self.db.commit()
            return True
        return False
