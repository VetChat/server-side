from typing import List, Type, Optional
from sqlalchemy.orm import Session
from app.models import Symptom, QuestionSet


class SymptomCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_symptoms(self) -> List[Type[Symptom]]:
        return self.db.query(Symptom).all()

    def fetch_symptom_by_id(self, symptom_id: int) -> Optional[Type[Symptom]]:
        return self.db.query(Symptom).filter(Symptom.symptom_id == symptom_id).first()

    def fetch_symptom_by_name(self, symptom_name: str) -> Optional[Type[Symptom]]:
        return self.db.query(Symptom).filter(Symptom.symptom_name == symptom_name).first()

    def fetch_symptoms_by_animal_id(self, animal_id: int):
        return (
            self.db.query(Symptom.symptom_id, Symptom.symptom_name, QuestionSet.question_set_id)
            .join(QuestionSet.symptom)
            .filter(QuestionSet.animal_id == animal_id)
            .all()
        )

    def add_symptom(self, symptom_name: str) -> Symptom:
        new_symptom = Symptom(symptom_name=symptom_name)
        self.db.add(new_symptom)
        self.db.commit()
        self.db.refresh(new_symptom)
        return new_symptom

    def update_symptom(self, symptom_id: int, symptom_name: str) -> Optional[Type[Symptom]]:
        symptom = self.fetch_symptom_by_id(symptom_id)
        if symptom:
            symptom.symptom_name = symptom_name
            self.db.commit()
            self.db.refresh(symptom)
            return symptom
        return None

    def remove_symptom(self, symptom_id: int) -> bool:
        symptom = self.fetch_symptom_by_id(symptom_id)
        if symptom:
            self.db.delete(symptom)
            self.db.commit()
            return True
        return False
