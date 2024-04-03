from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from ..models import AnswerRecord, Answer, Question, Symptom, QuestionSet


class AnswerRecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_answer_data_by_ids(self, answer_ids: List[int]):
        return (
            self.db.query(Answer.question_id,
                          Answer.answer,
                          Answer.summary,
                          Answer.skip_to_question,
                          Question.question,
                          Question.pattern,
                          Question.image_path,
                          Question.ordinal,
                          Symptom.symptom_id,
                          Symptom.symptom_name)
            .join(Answer.question)
            .join(Question.question_set)
            .join(QuestionSet.symptom)
            .filter(Answer.answer_id.in_(answer_ids))
            .order_by(Symptom.symptom_id, Question.ordinal)
            .all()
        )

    def create_answer_records(self, ticket_id: int, answer_data: List[dict]):
        # Create answer records
        for answer in answer_data:
            answer_record = AnswerRecord(
                ticket_id=ticket_id,
                symptom_id=answer.symptom_id,
                symptom_name=answer.symptom_name,
                question=answer.question,
                image_path=answer.image_path,
                ordinal=answer.ordinal,
                answer=answer.answer,
                summary=answer.summary
            )
            self.db.add(answer_record)
        self.db.commit()
