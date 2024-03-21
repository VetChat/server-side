from typing import List, Type

from sqlalchemy.orm import Session
from ..models import Symptom


class SymptomCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_symptoms(self) -> List[Type[Symptom]]:
        return self.db.query(Symptom).all()

    def fetch_symptom_by_name(self, symptom_name: str) -> Type[Symptom]:
        return self.db.query(Symptom).filter(Symptom.symptom_name == symptom_name).first()

    def add_symptom(self, symptom_name: str) -> Symptom:
        new_symptom = Symptom(symptom_name=symptom_name)
        self.db.add(new_symptom)
        self.db.commit()
        self.db.refresh(new_symptom)
        return new_symptom
