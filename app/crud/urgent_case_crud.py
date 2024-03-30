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
            self.db.query(UrgentCase.urgent_id, UrgentCase.urgent_name, UrgentCase.urgency_id)
            .all()
        )

    def fetch_urgent_case_by_animal_id(self, animal_id: int):
        return (
            self.db.query(UrgentCase.urgent_id, UrgentCase.urgent_name, UrgentCase.urgency_id)
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

    def fetch_urgent_case_by_name(self, animal_id: int, urgent_case: UrgentCaseCreate):
        return (
            self.db.query(UrgentCase)
            .filter(and_(UrgentCase.animal_id == animal_id, UrgentCase.urgent_name == urgent_case.urgent_name))
            .first()
        )

    def fetch_urgent_case_with_urgency_detail(self):
        return (
            self.db.query(UrgentCase.urgent_id, UrgentCase.urgent_name, Urgency.urgency_detail, Urgency.duration)
            .join(UrgentCase.urgency)
            .all()
        )

    def add_urgent_case(self, urgent_name: str, urgency_id: int):
        new_urgent_case = UrgentCase(
            urgent_name=urgent_name,
            urgency_id=urgency_id
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

    def update_multiple_urgent_cases(self, updates: List[UrgentCaseUpdate]) -> Optional[List[Type[UrgentCase]]]:
        urgent_ids = [update.urgent_id for update in updates]
        urgent_cases = self.fetch_urgent_case_by_ids(urgent_ids)
        if urgent_cases is None:
            return None
        urgent_case_mapping = {urgent_case.urgent_id: urgent_case for urgent_case in urgent_cases}

        for update in updates:
            if update.urgent_id in urgent_case_mapping:
                urgent_case = urgent_case_mapping[update.urgent_id]
                urgent_case.urgent_name = update.urgent_name
                urgent_case.urgency_id = update.urgency_id

        self.db.commit()

        # Optionally refresh the state of each updated UrgentCase
        for urgent_case in urgent_cases:
            self.db.refresh(urgent_case)

        return urgent_cases

    def remove_urgent_case(self, urgent_id: int):
        urgent_case = self.fetch_urgent_case_by_id(urgent_id)
        if not urgent_case:
            return None
        self.db.delete(urgent_case)
        self.db.commit()
        return urgent_case
