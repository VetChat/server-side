import json
from typing import List, Optional
from fastapi import Request, APIRouter, Depends, HTTPException, UploadFile, Form
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from collections import defaultdict

from app.aws import S3Resource
from app.schemas.question_schema import QuestionWithListAnswerUpdateResponse, QuestionId, QuestionDeleteBulkResponse
from app.utils import limiter, format_file_name
from app.database import get_db
from app.crud import QuestionCRUD, AnswerCRUD, QuestionSetCRUD
from app.schemas import QuestionSetRequest, QuestionResponse, AnswerRead, QuestionWithListAnswer, \
    QuestionWithListAnswerCreate, AnswerCreateBulkResponse, AnswerResponse, AnswerCreateFailed, \
    QuestionCreateBulkResponse, \
    QuestionWithListAnswerCreateResponse, QuestionWithListAnswerUpdate, QuestionWithListAnswerDeleteResponse, \
    QuestionCreateFailedResponse, AnswerCreate, AnswerUpdate, QuestionUpdateBulkResponse, QuestionUpdateFailedResponse, \
    AnswerUpdateFailed, AnswerUpdateBulkResponse


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(generate_unique_id_function=custom_generate_unique_id)

s3 = S3Resource()


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
                    listAnswer=[] if question.Question.pattern == 'text' else [
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


@router.post("/question_set/question", response_model=QuestionWithListAnswerCreateResponse, tags=["Question"])
@limiter.limit("10/minute")
async def create_question(request: Request, question_str: str = Form(...),
                          image: Optional[UploadFile] = None,
                          db: Session = Depends(get_db)) -> QuestionWithListAnswerCreateResponse:
    # Manually parse the question JSON string
    try:
        question_dict = json.loads(question_str)
        question = QuestionWithListAnswerCreate(**question_dict)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"JSON Decode Error: {e.msg}")

    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_question_by_question_and_question_set_id(question.question,
                                                                                  question.questionSetId)

    question_set_crud = QuestionSetCRUD(db)
    question_set_data = question_set_crud.fetch_question_set_info_by_id(question.questionSetId)

    if questions_data:
        raise HTTPException(status_code=409,
                            detail=f"Question with ID {question.question} in this question set already exists")

    if question.haveImage and image is not None:
        image_path = await s3.upload_file_to_s3(image, question_set_data.animal.animal_name,
                                                question_set_data.symptom.symptom_name, question.question)
        question.imagePath = image_path

    question_data = question_crud.create_question(question.questionSetId, question.question, question.pattern,
                                                  question.ordinal, question.imagePath)

    if not question_data:
        raise HTTPException(status_code=500, detail="Failed to add the question")

    answer_crud = AnswerCRUD(db)

    answer_result = create_answer(answer_crud, question_data.question_id, question.listAnswer)

    return QuestionWithListAnswerCreateResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=answer_result,
        message="Question added successfully"
    )


@router.post("/question_set/question/bulk", response_model=QuestionCreateBulkResponse, tags=["Question"])
@limiter.limit("2/minute")
async def create_questions(request: Request, questions_data: str = Form(...),
                           images: List[Optional[UploadFile]] = None,
                           db: Session = Depends(get_db)) -> QuestionCreateBulkResponse:
    questions = json.loads(questions_data)

    question_crud = QuestionCRUD(db)
    answer_crud = AnswerCRUD(db)
    question_set_crud = QuestionSetCRUD(db)

    question_result = QuestionCreateBulkResponse(success=[], failed=[])
    for question_dict in questions:
        try:
            q = QuestionWithListAnswerCreate(**question_dict)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"JSON Decode Error: {e.msg}")

        questions_data = question_crud.fetch_question_by_question_and_question_set_id(q.question, q.questionSetId)

        if questions_data:
            question_result.failed.append(
                QuestionCreateFailedResponse(
                    question=q.question,
                    pattern=q.pattern,
                    imagePath=q.imagePath,
                    ordinal=q.ordinal,
                    message="Question already exists"
                )
            )
            continue

        if q.haveImage:
            await upload_image_to_s3(question_set_crud, images, q)

        question_data = question_crud.create_question(q.questionSetId, q.question, q.pattern, q.ordinal, q.imagePath)

        if not question_data:
            question_result.failed.append(
                QuestionCreateFailedResponse(
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
            QuestionWithListAnswerCreateResponse(
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


@router.put("/question_set/question", response_model=QuestionWithListAnswerCreateResponse, tags=["Question"])
@limiter.limit("20/minute")
async def update_question(request: Request, question: QuestionWithListAnswerUpdate,
                          db: Session = Depends(get_db)) -> QuestionWithListAnswerCreateResponse:
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
    answer_result = update_answer(answer_crud, question.listAnswer)

    return QuestionWithListAnswerCreateResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=answer_result,
        message="Question updated successfully"
    )


@router.put("/question_set/question/bulk", response_model=QuestionUpdateBulkResponse, tags=["Question"])
@limiter.limit("5/minute")
async def update_questions(request: Request, questions_data: str = Form(...),
                           images: List[UploadFile] = None,
                           db: Session = Depends(get_db)) -> QuestionUpdateBulkResponse:
    questions = json.loads(questions_data)

    question_crud = QuestionCRUD(db)
    answer_crud = AnswerCRUD(db)
    question_set_crud = QuestionSetCRUD(db)

    question_result = QuestionUpdateBulkResponse(success=[], failed=[])

    for question_dict in questions:
        try:
            q = QuestionWithListAnswerUpdate(**question_dict)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"JSON Decode Error: {e.msg}")

        question_data = question_crud.fetch_question_by_id(q.questionId)

        if not question_data:
            question_result.failed.append(
                QuestionUpdateFailedResponse(
                    questionId=q.question_id,
                    question=q.question,
                    pattern=q.pattern,
                    imagePath=q.imagePath,
                    ordinal=q.ordinal,
                    message="Question not found"
                )
            )
            continue

        if q.haveImage:
            await upload_image_to_s3(question_set_crud, images, q)

        question_data = question_crud.update_question(q.questionId, q.question, q.pattern, q.ordinal, q.imagePath)

        if not question_data:
            question_result.failed.append(
                QuestionUpdateFailedResponse(
                    questionId=q.question_id,
                    question=q.question,
                    pattern=q.pattern,
                    imagePath=q.imagePath,
                    ordinal=q.ordinal,
                    message="Failed to update the question"
                )
            )
            continue

        answer_result = update_answer(answer_crud, q.listAnswer)

        question_result.success.append(
            QuestionWithListAnswerUpdateResponse(
                questionId=question_data.question_id,
                question=question_data.question,
                pattern=question_data.pattern,
                imagePath=question_data.image_path,
                ordinal=question_data.ordinal,
                listAnswer=answer_result,
                message="Question updated successfully"
            )
        )

    return question_result


@router.delete("/question_set/question/bulk", response_model=QuestionDeleteBulkResponse, tags=["Question"])
@limiter.limit("2/minute")
async def delete_questions(request: Request, question_ids: List[QuestionId],
                           db: Session = Depends(get_db)) -> QuestionDeleteBulkResponse:
    question_crud = QuestionCRUD(db)
    questions_data = question_crud.fetch_question_by_list_id([q.questionId for q in question_ids])

    if len(questions_data) != len(question_ids):
        raise HTTPException(status_code=404, detail=f"One or more question id not found")

    answer_crud = AnswerCRUD(db)

    question_result = QuestionDeleteBulkResponse(success=[], failed=[])
    for q in question_ids:
        question_data = question_crud.fetch_question_by_id(q.questionId)
        answers = question_data.answers

        for answer in answers:
            is_success = answer_crud.delete_answer(answer.answer_id)
            if not is_success:
                question_result.failed.append(
                    QuestionUpdateFailedResponse(
                        questionId=question_data.question_id,
                        question=question_data.question,
                        pattern=question_data.pattern,
                        imagePath=question_data.image_path,
                        ordinal=question_data.ordinal,
                        message=f"Failed to delete the answer with ID {answer.answer_id}"
                    )
                )
                continue

        if question_data.image_path:
            is_success = await s3.remove_file_from_s3(question_data.image_path)
            if not is_success:
                question_result.failed.append(
                    QuestionUpdateFailedResponse(
                        questionId=question_data.question_id,
                        question=question_data.question,
                        pattern=question_data.pattern,
                        imagePath=question_data.image_path,
                        ordinal=question_data.ordinal,
                        message="Failed to delete the image"
                    )
                )
                continue

        is_success = question_crud.delete_question(question_data.question_id)

        if not is_success:
            question_result.failed.append(
                QuestionUpdateFailedResponse(
                    questionId=question_data.question_id,
                    question=question_data.question,
                    pattern=question_data.pattern,
                    imagePath=question_data.image_path,
                    ordinal=question_data.ordinal,
                    message="Failed to delete the question"
                )
            )
            continue

        question_result.success.append(
            QuestionWithListAnswerDeleteResponse(
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
        )

    return question_result


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


def create_answer(answer_crud: AnswerCRUD, question_id: int, answers: List[AnswerCreate]) -> AnswerCreateBulkResponse:
    answer_result = AnswerCreateBulkResponse(success=[], failed=[])

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


def update_answer(answer_crud: AnswerCRUD, answers: List[AnswerUpdate]) -> AnswerUpdateBulkResponse:
    answer_result = AnswerUpdateBulkResponse(success=[], failed=[])

    for answer in answers:
        existed_answers = answer_crud.fetch_answer_by_id(answer.answerId)
        if not existed_answers:
            answer_result.failed.append(
                AnswerUpdateFailed(
                    answerId=answer.answerId,
                    answer=answer.answer,
                    summary=answer.summary,
                    skipToQuestion=answer.skipToQuestion,
                    message="Answer not found"
                )
            )
            continue

        answer_data = answer_crud.update_answer(answer.answerId, answer.answer, answer.summary, answer.skipToQuestion)

        if answer_data:
            answer_result.success.append(
                AnswerResponse(
                    answerId=answer_data.answer_id,
                    answer=answer_data.answer,
                    summary=answer_data.summary,
                    skipToQuestion=answer_data.skip_to_question,
                    message="Answer updated successfully"
                )
            )
        else:
            answer_result.failed.append(
                AnswerUpdateFailed(
                    answerId=answer.answerId,
                    answer=answer.answer,
                    summary=answer.summary,
                    skipToQuestion=answer.skipToQuestion,
                    message="Failed to update the answer"
                )
            )

    return answer_result


async def upload_image_to_s3(question_set_crud: QuestionSetCRUD, images: List[UploadFile],
                             question: QuestionWithListAnswerCreate or QuestionWithListAnswerUpdate) -> Optional[str]:
    if question is QuestionWithListAnswerCreate:
        question_set_data = question_set_crud.fetch_question_set_info_by_id(question.questionSetId)
    else:
        question_set_data = question_set_crud.fetch_question_set_info_by_question_id(question.questionId)

    for image in images:
        file_name = image.filename.split(".")[0]
        file_extension = image.filename.split(".")[-1]

        question_formatted = format_file_name(question.question)

        if file_name != question_formatted:
            continue
        if file_extension not in ["jpg", "jpeg", "png"]:
            images.remove(image)
            continue

        image_path = await s3.upload_file_to_s3(image, question_set_data.animal.animal_name,
                                                question_set_data.symptom.symptom_name, question.question)
        question.imagePath = image_path

        images.remove(image)
        return image_path
