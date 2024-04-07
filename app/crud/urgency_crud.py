from typing import List
from sqlalchemy.orm import Session
from ..models import Urgency


class UrgencyCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_all_urgency(self):
        return self.db.query(Urgency).all()

    def fetch_urgency_levels_by_ids(self, urgency_ids: List[int]):
        return (
            self.db.query(Urgency)
            .filter(Urgency.urgency_id.in_(urgency_ids))
            .all()
        )
