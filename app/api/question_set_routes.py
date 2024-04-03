from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import QuestionList, AnswerRead, QuestionSetCreateBody, QuestionSetResponse
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


@router.post("/question_set", response_model=QuestionSetResponse, tags=["Question Set"])
@limiter.limit("5/minute")
async def add_question_set(request: Request, create_body: QuestionSetCreateBody, db: Session = Depends(get_db)) \
        -> QuestionSetResponse:
    question_set_crud = QuestionSetCRUD(db)
    existing_question_set = question_set_crud.fetch_question_set_by_symptom_animal_id(create_body.symptomId,
                                                                                      create_body.animalId)

    if existing_question_set:
        raise HTTPException(status_code=409,
                            detail=f"Question set with symptom id {create_body.symptomId} and animal id {create_body.animalId} already exists")

    question_set_data = question_set_crud.create_question_set(create_body.symptomId, create_body.animalId)

    return QuestionSetResponse(
        questionSetId=question_set_data.question_set_id,
        symptomId=question_set_data.symptom_id,
        animalId=question_set_data.animal_id,
        message="The question set has been successfully added."
    )
