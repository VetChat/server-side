from sqlalchemy.orm import Session
from ..models import UrgentCase, Urgency


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

    def fetch_urgent_case_with_urgency_detail(self):
        return (
            self.db.query(UrgentCase.urgent_id, UrgentCase.urgent_name, Urgency.urgency_detail, Urgency.duration)
            .join(UrgentCase.urgency)
            .all()
        )
