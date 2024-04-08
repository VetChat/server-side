from typing import List, Type, Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models import UrgentCase, Urgency
from app.schemas import UrgentCaseCreate, UrgentCaseUpdate


class UrgentCaseCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_all_urgent_case(self):
        return (
            self.db.query(UrgentCase.urgent_id,
                          UrgentCase.urgent_name,
                          UrgentCase.urgency_id,
                          Urgency.urgency_detail,
                          Urgency.duration,
                          Urgency.urgency_level)
            .join(UrgentCase.urgency)
            .all()
        )

    def fetch_urgent_case_by_animal_id(self, animal_id: int):
        return (
            self.db.query(UrgentCase.urgent_id,
                          UrgentCase.urgent_name,
                          UrgentCase.urgency_id,
                          Urgency.urgency_detail,
                          Urgency.duration,
                          Urgency.urgency_level)
            .join(UrgentCase.urgency)
            .filter(UrgentCase.animal_id == animal_id)
            .order_by(Urgency.urgency_level)
            .all()
        )

    def fetch_urgent_case_by_id(self, urgent_id: int):
        return (
            self.db.query(UrgentCase)
            .filter(UrgentCase.urgent_id == urgent_id)
            .first()
        )

    def fetch_urgent_case_by_ids(self, urgent_ids: List[int]):
        return (
            self.db.query(UrgentCase)
            .filter(UrgentCase.urgent_id.in_(urgent_ids))
            .all()
        )

    def fetch_urgent_case_by_name(self, animal_id: int, urgent_name: str):
        return (
            self.db.query(UrgentCase)
            .filter(and_(UrgentCase.animal_id == animal_id, UrgentCase.urgent_name == urgent_name))
            .first()
        )

    def fetch_urgent_cases_by_name(self, animal_id: int, urgent_names: List[str]):
        return (
            self.db.query(UrgentCase)
            .filter(and_(UrgentCase.animal_id == animal_id, UrgentCase.urgent_name.in_(urgent_names)))
            .first()
        )

    def fetch_urgent_case_with_urgency_detail(self):
        return (
            self.db.query(UrgentCase.urgent_id, UrgentCase.urgent_name, Urgency.urgency_detail, Urgency.duration)
            .join(UrgentCase.urgency)
            .all()
        )

    def add_urgent_case(self, urgent_name: str, urgency_id: int, animal_id: int):
        new_urgent_case = UrgentCase(
            urgent_name=urgent_name,
            urgency_id=urgency_id,
            animal_id=animal_id
        )
        self.db.add(new_urgent_case)
        self.db.commit()
        self.db.refresh(new_urgent_case)
        return new_urgent_case

    def update_urgent_case(self, urgent_id: int, urgent_name: str, urgency_id: int):
        urgent_case = self.fetch_urgent_case_by_id(urgent_id)
        if not urgent_case:
            return None
        urgent_case.urgent_name = urgent_name
        urgent_case.urgency_id = urgency_id
        self.db.commit()
        self.db.refresh(urgent_case)
        return urgent_case

    def remove_urgent_case(self, urgent_id: int):
        urgent_case = self.fetch_urgent_case_by_id(urgent_id)
        if not urgent_case:
            return None
        self.db.delete(urgent_case)
        self.db.commit()
        return urgent_case
