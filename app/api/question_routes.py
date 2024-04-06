from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from app.schemas.question_schema import QuestionWithListAnswerResponse
from app.utils import limiter
from app.database import get_db
from app.crud import QuestionCRUD, AnswerCRUD
from app.schemas import QuestionSetRequest, QuestionResponse, AnswerRead, QuestionWithListAnswer, \
    QuestionWithListAnswerCreate, AnswerBulkResponse, AnswerResponse, AnswerCreateFailed

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


@router.post("/question_set/question", response_model=QuestionWithListAnswerResponse, tags=["Question"])
@limiter.limit("10/minute")
async def create_question_by_set_id(request: Request, question: QuestionWithListAnswerCreate,
                                    db: Session = Depends(get_db)) -> QuestionWithListAnswerResponse:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_question_by_question_and_question_set_id(question.question,
                                                                                  question.questionSetId)

    if questions_data:
        raise HTTPException(status_code=409,
                            detail=f"Question with ID {question.question} in this question set already exists")

    question_data = question_crud.create_question(question.questionSetId, question.question, question.pattern,
                                                  question.ordinal, question.imagePath)

    if not question_data:
        raise HTTPException(status_code=500, detail="Failed to add the question")

    answer_crud = AnswerCRUD(db)
    existed_answers = answer_crud.fetch_answer_by_question_id_and_answer(question_data.question_id,
                                                                         [a.answer for a in question.listAnswer])

    if existed_answers:
        raise HTTPException(status_code=409,
                            detail=f"Answers for question with ID {question.questionId} already exists")

    answer_success = []
    answer_failed = []
    for answer in question.listAnswer:
        answer_data = answer_crud.create_answer(question_data.question_id, answer.answer, answer.summary,
                                                answer.skipToQuestion)
        if answer_data:
            answer_success.append(
                AnswerResponse(
                    answerId=answer_data.answer_id,
                    answer=answer_data.answer,
                    summary=answer_data.summary,
                    skipToQuestion=answer_data.skip_to_question,
                    message="Answer added successfully"
                )
            )
        else:
            answer_failed.append(
                AnswerCreateFailed(
                    answer=answer_data.answer,
                    message="Failed to add the answer"
                )
            )
    answer_data = AnswerBulkResponse(success=answer_success if answer_success else None,
                                     failed=None if not answer_failed else answer_failed)

    return QuestionWithListAnswerResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=AnswerBulkResponse(success=answer_success if answer_success else None,
                                      failed=None if not answer_failed else answer_failed)
    )
