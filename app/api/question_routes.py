from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from app.utils import limiter
from app.database import get_db
from app.crud import QuestionCRUD
from app.schemas import QuestionSetRequest, QuestionResponse, AnswerRead, QuestionWithListAnswer, \
    QuestionWintListAnswerCreate

router = APIRouter()


@router.post("/questions/question_set_ids", response_model=List[QuestionResponse], tags=["Question"])
@limiter.limit("10/minute")
async def get_questions_by_set_ids(request: Request, question: List[QuestionSetRequest], db: Session = Depends(get_db)) \
        -> List[QuestionResponse]:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_questions_by_set_ids([rq.questionSetId for rq in question])

    if not questions_data:
        raise HTTPException(status_code=404, detail="No questions found for the provided question set IDs")

    # Group questions by symptom
    symptom_groups = defaultdict(list)

    for item in questions_data:
        symptom_groups[(item.symptom_id, item.symptom_name)].append(item)

    # Transform the data into the desired response format
    questions_response = [
        QuestionResponse(
            symptomId=symptom_id,
            symptomName=symptom_name,
            listQuestion=[
                QuestionWithListAnswer(
                    questionId=question.Question.question_id,
                    question=question.Question.question,
                    pattern=question.Question.pattern,
                    imagePath=question.Question.image_path,
                    ordinal=question.Question.ordinal,
                    listAnswer=[
                        AnswerRead(
                            answerId=answer.answer_id,
                            answer=answer.answer,
                            summary=answer.summary,
                            skipToQuestion=answer.skip_to_question
                        ) for answer in question.Question.answers
                    ]
                )
                for question in questions
            ]
        )
        for (symptom_id, symptom_name), questions in symptom_groups.items()
    ]

    return questions_response


@router.post("/question_set/question", response_model=List[QuestionResponse], tags=["Question"])
@limiter.limit("10/minute")
async def create_question_by_set_id(request: Request, question: QuestionWintListAnswerCreate,
                                    db: Session = Depends(get_db)) -> QuestionWithListAnswer:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_question_by_question_id_and_question_set_id(question.questionId,
                                                                                     question.questionSetId)

    if questions_data:
        raise HTTPException(status_code=409, detail=f"Question with ID {question.questionId} already exists")

    question_data = question_crud.create_question(question.questionSetId, question.question, question.pattern,
                                                  question.ordinal, question.imagePath)
    
    # Transform the data into the desired response format
    questions_response = [
        QuestionResponse(
            symptomId=symptom_id,
            symptomName=symptom_name,
            listQuestion=[
                QuestionWithListAnswer(
                    questionId=question.Question.question_id,
                    question=question.Question.question,
                    pattern=question.Question.pattern,
                    imagePath=question.Question.image_path,
                    ordinal=question.Question.ordinal,
                    listAnswer=[
                        AnswerRead(
                            answerId=answer.answer_id,
                            answer=answer.answer,
                            summary=answer.summary,
                            skipToQuestion=answer.skip_to_question
                        ) for answer in question.Question.answers
                    ]
                )
                for question in questions
            ]
        )
        for (symptom_id, symptom_name), questions in symptom_groups.items()
    ]

    return questions_response
