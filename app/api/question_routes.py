from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from app.utils import limiter
from app.database import get_db
from app.crud import QuestionCRUD, AnswerCRUD
from app.schemas import QuestionSetRequest, QuestionResponse, AnswerRead, QuestionWithListAnswer, \
    QuestionWithListAnswerCreate, AnswerBulkResponse, AnswerResponse, AnswerCreateFailed, QuestionBulkResponse, \
    QuestionWithListAnswerResponse, QuestionWithListAnswerUpdate, QuestionWithListAnswerDeleteResponse, \
    QuestionFailedResponse, AnswerCreate

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
async def create_question(request: Request, question: QuestionWithListAnswerCreate,
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

    answer_result = create_answer(answer_crud, question_data.question_id, questions_data.listAnswer)

    return QuestionWithListAnswerResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=answer_result,
        message="Question added successfully"
    )


@router.post("/question_set/question/bulk", response_model=QuestionBulkResponse, tags=["Question"])
@limiter.limit("10/minute")
async def create_question(request: Request, question: List[QuestionWithListAnswerCreate],
                          db: Session = Depends(get_db)) -> QuestionBulkResponse:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_questions_by_questions_and_question_set_id([q.question for q in question],
                                                                                    question[0].questionSetId)

    if questions_data:
        raise HTTPException(status_code=409,
                            detail=f"Questions in this question set already exists")

    answer_crud = AnswerCRUD(db)

    question_result = QuestionBulkResponse(success=[], failed=[])
    for q in question:
        question_data = question_crud.create_question(q.questionSetId, q.question, q.pattern, q.ordinal, q.imagePath)

        if not question_data:
            question_result.failed.append(
                QuestionFailedResponse(
                    question=q.question,
                    pattern=q.pattern,
                    imagePath=q.imagePath,
                    ordinal=q.ordinal,
                    message="Failed to add the question"
                )
            )
            continue

        answer_result = create_answer(answer_crud, question_data.question_id, q.listAnswer)

        question_result.success.append(
            QuestionWithListAnswerResponse(
                questionId=question_data.question_id,
                question=question_data.question,
                pattern=question_data.pattern,
                imagePath=question_data.image_path,
                ordinal=question_data.ordinal,
                listAnswer=answer_result,
                message="Question added successfully"
            )
        )

    return question_result


@router.put("/question_set/question", response_model=QuestionWithListAnswerResponse, tags=["Question"])
@limiter.limit("20/minute")
async def update_question(request: Request, question: QuestionWithListAnswerUpdate,
                          db: Session = Depends(get_db)) -> QuestionWithListAnswerResponse:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_question_by_id(question.questionId)

    if not questions_data:
        raise HTTPException(status_code=404,
                            detail=f"Question with ID {question.question} in this question set not found")

    question_data = question_crud.update_question(questions_data.question_id, question.question, question.pattern,
                                                  question.ordinal, question.imagePath)

    if not question_data:
        raise HTTPException(status_code=500, detail="Failed to update the question")

    answer_crud = AnswerCRUD(db)
    existed_answers = answer_crud.fetch_answer_by_question_id_and_answer(question_data.question_id,
                                                                         [a.answer for a in question.listAnswer])

    if existed_answers:
        raise HTTPException(status_code=409,
                            detail=f"Answers for question with ID {question.questionId} already exists")

    answer_result = AnswerBulkResponse(success=[], failed=[])
    for answer in question.listAnswer:
        answer_data = answer_crud.update_answer(answer.answerId, answer.answer, answer.summary,
                                                answer.skipToQuestion)
        if answer_data:
            answer_result.success.append(
                AnswerResponse(
                    answerId=answer_data.answer_id,
                    answer=answer_data.answer,
                    summary=answer_data.summary,
                    skipToQuestion=answer_data.skip_to_question,
                    message="Answer added successfully"
                )
            )
        else:
            answer_result.failed.append(
                AnswerCreateFailed(
                    answer=answer.answer,
                    message="Failed to add the answer"
                )
            )

    return QuestionWithListAnswerResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=answer_result,
        message="Question updated successfully"
    )


@router.delete("/question_set/question/{question_id}", response_model=QuestionWithListAnswerDeleteResponse,
               tags=["Question"])
@limiter.limit("10/minute")
async def delete_question(request: Request, question_id: int,
                          db: Session = Depends(get_db)) -> QuestionWithListAnswerDeleteResponse:
    question_crud = QuestionCRUD(db)
    question_data = question_crud.fetch_question_by_id(question_id)

    if not question_data:
        raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found")

    answers = question_data.answers

    answer_crud = AnswerCRUD(db)
    for answer in answers:
        is_success = answer_crud.delete_answer(answer.answer_id)
        if not is_success:
            raise HTTPException(status_code=500, detail=f"Failed to delete the answer with ID {answer.answer_id}")

    is_success = question_crud.delete_question(question_data.question_id)

    if not is_success:
        raise HTTPException(status_code=500, detail="Failed to delete the question")

    return QuestionWithListAnswerDeleteResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=[
            AnswerRead(
                answerId=answer.answer_id,
                answer=answer.answer,
                summary=answer.summary,
                skipToQuestion=answer.skip_to_question
            ) for answer in answers
        ],
        message="Question deleted successfully"
    )


def create_answer(answer_crud: AnswerCRUD, question_id: int, answers: List[AnswerCreate]) -> AnswerBulkResponse:
    answer_result = AnswerBulkResponse(success=[], failed=[])

    for answer in answers:
        existed_answers = answer_crud.fetch_answer_by_question_id_and_answer(question_id, answer.answer)
        if existed_answers:
            answer_result.failed.append(
                AnswerCreateFailed(
                    answer=answer.answer,
                    message="Answer already exists"
                )
            )
            continue

        answer_data = answer_crud.create_answer(question_id, answer.answer, answer.summary, answer.skipToQuestion)
        if answer_data:
            answer_result.success.append(
                AnswerResponse(
                    answerId=answer_data.answer_id,
                    answer=answer_data.answer,
                    summary=answer_data.summary,
                    skipToQuestion=answer_data.skip_to_question,
                    message="Answer added successfully"
                )
            )
        else:
            answer_result.failed.append(
                AnswerCreateFailed(
                    answer=answer.answer,
                    message="Failed to add the answer"
                )
            )
    return answer_result
