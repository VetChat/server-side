from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils import limiter
from ..database import get_db
from ..crud import QuestionCRUD
from ..schemas import QuestionSetRequest, QuestionResponse, AnswerRead

router = APIRouter()


@router.post("/questions/question_set_ids", response_model=List[QuestionResponse], tags=["Question"])
@limiter.limit("10/minute")
async def get_questions_by_set_ids(request: Request, question: List[QuestionSetRequest], db: Session = Depends(get_db)) \
        -> List[QuestionResponse]:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_questions_by_set_ids([rq.questionSetId for rq in question])

    if not questions_data:
        raise HTTPException(status_code=404, detail="No questions found for the provided question set IDs")

    # Transform the data into the desired response format
    questions_response = [
        QuestionResponse(
            symptomId=symptom_id,
            symptomName=symptom_name,
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
        for question, symptom_id, symptom_name in questions_data
    ]

    return questions_response
