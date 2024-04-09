from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from ..models import AnswerRecord, Answer, Question, Symptom, QuestionSet


class AnswerRecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_answer_data_by_question_id_and_answer(self, question_id: id, answer: str):
        result = (
            self.db.query(Question.question_id,
                          Question.question,
                          Question.pattern,
                          Question.image_path,
                          Question.ordinal,
                          Symptom.symptom_id,
                          Symptom.symptom_name,
                          Answer.answer,
                          Answer.summary,
                          Answer.skip_to_question)
            .join(Question.question_set)
            .join(QuestionSet.symptom)
            .outerjoin(Question.answers)
            .filter(Question.question_id == question_id,
                    (Answer.answer == answer) | (Question.pattern == 'text'))
            .order_by(Symptom.symptom_id, Question.ordinal)
            .first()
        )

        if result and result.pattern == 'text':
            result.answer = answer

        return result

    def create_answer_records(self, ticket_id: int, answer_data: List[dict]):
        try:
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
            # Commit all changes at once
            self.db.commit()
        except Exception as e:
            # Rollback all changes if an error occurs
            self.db.rollback()
            raise e
