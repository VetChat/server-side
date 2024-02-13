from typing import Type, List, Optional
from sqlalchemy.orm import Session
from ..models import UrgentCase, Urgency


class UrgentCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_all_urgent_case(self):
        return (
            self.db.query(UrgentCase.urgent_id, UrgentCase.urgent_name, Urgency.urgency_detail, Urgency.duration)
            .join(Urgency, UrgentCase.urgency_id == Urgency.urgency_id)
            .all()
        )

    def fetch_urgent_case_by_animal_id(self, animal_id: int):
        return (
            self.db.query(UrgentCase.urgent_id, UrgentCase.urgent_name, Urgency.urgency_detail, Urgency.duration)
            .join(Urgency, UrgentCase.urgency_id == Urgency.urgency_id)
            .filter(UrgentCase.animal_id == animal_id)
            .all()
        )
