from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud.question_crud import QuestionCRUD
from ..schemas import QuestionSetRequest, QuestionResponse

router = APIRouter()


@router.post("/questions/by_set_ids", response_model=List[QuestionResponse])
def get_questions_by_set_ids(request: QuestionSetRequest, db: Session = Depends(get_db)) -> List[QuestionResponse]:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.get_questions_by_set_ids(request.question_set_ids)

    if not questions_data:
        raise HTTPException(status_code=404, detail="No questions found for the provided question set IDs")

    # Transform the data into the desired response format
    questions_response = [
        QuestionResponse(
            symptom_id=symptom_id,
            symptom_name=symptom_name,
            question_id=question.question_id,
            question=question.question,
            pattern=question.pattern,
            image_path=question.image_path,
            ordinal=question.ordinal
        )
        for question, symptom_id, symptom_name in questions_data
    ]

    return questions_response
