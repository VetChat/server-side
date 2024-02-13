from sqlalchemy.orm import Session
from ..models import Symptom


class SymptomCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_symptoms_by_animal_id(self, animal_id: int):
        return self.db.query(Symptom).filter(Symptom.animal_id == animal_id).all()
