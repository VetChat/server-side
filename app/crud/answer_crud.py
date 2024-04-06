from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models import Answer


class AnswerCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_answer_by_id(self, answer_id: int) -> Optional[Answer]:
        return self.db.query(Answer).filter(Answer.answer_id == answer_id).first()

    def fetch_answer_by_question_id_and_answer(self, question_id: int, answer: List[str]) -> Optional[Answer]:
        return self.db.query(Answer).filter(Answer.question_id == question_id, Answer.answer.in_(answer)).first()

    def create_answer(self, question_id: int, answer: str, summary: str, skip_to_question: int) -> Optional[Answer]:
        new_answer = Answer(
            question_id=question_id,
            answer=answer,
            summary=summary,
            skip_to_question=skip_to_question
        )
        try:
            self.db.add(new_answer)
            self.db.commit()
            self.db.refresh(new_answer)
            return new_answer
        except SQLAlchemyError:
            self.db.rollback()
            return None
