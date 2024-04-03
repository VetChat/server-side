from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import QuestionList, AnswerRead
from app.utils import limiter
from app.database import get_db
from app.crud import QuestionCRUD, QuestionSetCRUD

router = APIRouter()


@router.get("/question_set/{question_set_id}", response_model=List[QuestionList], tags=["Question Set"])
@limiter.limit("10/minute")
async def get_question_set_by_question_set_id(request: Request, question_set_id: int, db: Session = Depends(get_db)) \
        -> List[QuestionList]:
    question_set_crud = QuestionSetCRUD(db)
    question_set_data = question_set_crud.fetch_question_set_id_by_id(question_set_id)

    if not question_set_data:
        raise HTTPException(status_code=404, detail=f"Question set with id {question_set_id} not found")

    question_crud = QuestionCRUD(db)
    question_data = question_crud.fetch_questions_by_question_set_id(question_set_id)

    question_response = [
        QuestionList(
            questionId=question.question_id,
            question=question.question,
            pattern=question.pattern,
            imagePath=question.image_path,
            ordinal=question.ordinal,
            listAnswer=[
                AnswerRead(
                    answerId=answer.answer_id,
                    answer=answer.answer,
                    summary=answer.summary,
                    skipToQuestion=answer.skip_to_question
                ) for answer in question.answers
            ]
        )
        for question in question_data
    ]

    return question_response
