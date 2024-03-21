from sqlalchemy.orm import Session
from ..models import Symptom


class SymptomCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_symptoms(self):
        return self.db.query(Symptom).all()
