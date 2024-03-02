from sqlalchemy.orm import Session
from ..models import QuestionSet, Symptom


class QuestionSetCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_symptoms_by_animal_id(self, animal_id: int):
        return (
            self.db.query(Symptom.symptom_id, Symptom.symptom_name, QuestionSet.question_set_id)
            .join(QuestionSet.symptom)
            .filter(QuestionSet.animal_id == animal_id)
            .all()
        )
