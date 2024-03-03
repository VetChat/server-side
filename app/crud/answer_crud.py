from typing import Optional
from sqlalchemy.orm import Session
from ..models import Answer


class AnswerCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_answer_by_id(self, answer_id: int) -> Optional[Answer]:
        return self.db.query(Answer).filter(Answer.answer_id == answer_id).first()
