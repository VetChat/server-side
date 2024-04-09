import json
from typing import List, Optional, Any, Coroutine
from fastapi import Request, APIRouter, Depends, HTTPException, UploadFile, Form
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from collections import defaultdict

from app.aws import S3Resource
from app.schemas.question_schema import QuestionWithListAnswerCreateUpdate, QuestionCreateUpdateDelete, \
    QuestionCreateUpdateDeleteSuccessResponse, QuestionCreateUpdateDeleteFailedResponse
from app.utils import limiter, format_file_name
from app.database import get_db
from app.crud import QuestionCRUD, AnswerCRUD, QuestionSetCRUD
from app.schemas import QuestionSetRequest, QuestionResponse, AnswerRead, QuestionWithListAnswer, \
    QuestionWithListAnswerCreate, AnswerResponse, AnswerCreateFailed, QuestionWithListAnswerResponse, \
    QuestionWithListAnswerUpdate, QuestionWithListAnswerDeleteResponse, \
    QuestionCreateFailedResponse, QuestionUpdateFailedResponse, AnswerUpdateFailed, AnswerCreateUpdate, \
    AnswerCreateUpdateDeleteBulkResponse, AnswerCreateUpdateDelete, AnswerDeleteResponse, QuestionDeleteResponse, \
    QuestionCreateUpdateDeleteBulkResponse, AnswerCreateUpdateDeleteSuccessResponse, \
    AnswerCreateUpdateDeleteFailedResponse


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
                    listAnswer=[
                        AnswerRead(
                            answerId=answer.answer_id,
                            answer=answer.answer,
                            summary=answer.summary,
                            skipToQuestion=answer.skip_to_question
                        ) for answer in question.Question.answers if question.Question.pattern != 'text'
                    ]
                )
                for question in questions
            ]
        )
        for (symptom_id, symptom_name), questions in symptom_groups.items()
    ]

    return questions_response


@router.put("/question_set/question/bulk", response_model=QuestionCreateUpdateDeleteBulkResponse, tags=["Question"])
@limiter.limit("5/minute")
async def update_questions(request: Request, questions_data: str = Form(...),
                           images: Optional[List[UploadFile]] = None,
                           db: Session = Depends(get_db)) -> QuestionCreateUpdateDeleteBulkResponse:
    questions = json.loads(questions_data)

    question_crud = QuestionCRUD(db)
    answer_crud = AnswerCRUD(db)
    question_set_crud = QuestionSetCRUD(db)

    try:
        question_data = QuestionCreateUpdateDelete(**questions)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"JSON Decode Error: {e.msg}")

    return await create_update_delete_question(question_crud, question_set_crud, answer_crud, question_data, images)


async def create_update_delete_question(question_crud: QuestionCRUD, question_set_crud: QuestionSetCRUD,
                                        answer_crud: AnswerCRUD, question: QuestionCreateUpdateDelete,
                                        images: List[Optional[UploadFile]] = None) -> (
        QuestionCreateUpdateDeleteBulkResponse):
    success_model = QuestionCreateUpdateDeleteSuccessResponse(create=[], update=[], delete=[])
    failed_model = QuestionCreateUpdateDeleteFailedResponse(create=[], update=[], delete=[])

    question_result = QuestionCreateUpdateDeleteBulkResponse(success=success_model, failed=failed_model)

    for q in question.createUpdate:
        if q.questionId:
            result = await update_question(question_crud, question_set_crud, answer_crud, q, images)
        else:
            result = await create_question(question_crud, question_set_crud, answer_crud, q, images)

        if isinstance(result, QuestionWithListAnswerResponse):
            question_result.success.update.append(result)
        else:
            question_result.failed.update.append(result)

    for q in question.delete:
        result = await delete_question(question_crud, answer_crud, q.questionId)
        if isinstance(result, QuestionWithListAnswerDeleteResponse):
            question_result.success.delete.append(result)
        else:
            question_result.failed.delete.append(result)

    return question_result


async def create_question(question_crud: QuestionCRUD, question_set_crud: QuestionSetCRUD, answer_crud: AnswerCRUD,
                          question: QuestionWithListAnswerCreateUpdate, images: List[Optional[UploadFile]] = None) -> (
        QuestionCreateFailedResponse or QuestionWithListAnswerResponse):
    questions_data = question_crud.fetch_question_by_question_and_question_set_id(question.question,
                                                                                  question.questionSetId)

    if questions_data:
        return QuestionCreateFailedResponse(
            question=question.question,
            pattern=question.pattern,
            imagePath=question.imagePath,
            ordinal=question.ordinal,
            message="Question already exists"
        )

    if question.have_image:
        await upload_image_to_s3(question_set_crud, images, question)

    question_data = question_crud.create_question(question.questionSetId, question.question, question.pattern,
                                                  question.ordinal, question.imagePath)

    if not question_data:
        return QuestionCreateFailedResponse(
            question=question.question,
            pattern=question.pattern,
            imagePath=question.imagePath,
            ordinal=question.ordinal,
            message="Failed to add the question"
        )

    answer_result = create_update_delete_answer(answer_crud, question_data.question_id, question.listAnswer)

    return QuestionWithListAnswerResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=answer_result,
        message="Question added successfully"
    )


async def update_question(question_crud: QuestionCRUD, question_set_crud: QuestionSetCRUD, answer_crud: AnswerCRUD,
                          question: QuestionWithListAnswerCreateUpdate, images: List[Optional[UploadFile]] = None) -> (
        QuestionUpdateFailedResponse or QuestionWithListAnswerResponse):
    question_data = question_crud.fetch_question_by_id(question.questionId)

    if not question_data:
        return QuestionUpdateFailedResponse(
            questionId=question.question_id,
            question=question.question,
            pattern=question.pattern,
            imagePath=question.imagePath,
            ordinal=question.ordinal,
            message="Question not found"
        )

    if question.haveImage:
        await upload_image_to_s3(question_set_crud, images, question)
    elif not question.haveImage and question_data.image_path:
        is_success = await s3.remove_file_from_s3(question_data.image_path)
        if not is_success:
            return QuestionUpdateFailedResponse(
                questionId=question_data.question_id,
                question=question_data.question,
                pattern=question_data.pattern,
                imagePath=question_data.image_path,
                ordinal=question_data.ordinal,
                message="Failed to delete the image"
            )

    question_data = question_crud.update_question(question.questionId, question.question, question.pattern,
                                                  question.ordinal, question.imagePath)

    if not question_data:
        return QuestionUpdateFailedResponse(
            questionId=question.question_id,
            question=question.question,
            pattern=question.pattern,
            imagePath=question.imagePath,
            ordinal=question.ordinal,
            message="Failed to update the question"
        )

    answer_result = create_update_delete_answer(answer_crud, question.questionId, question.listAnswer)

    return QuestionWithListAnswerResponse(
        questionId=question_data.question_id,
        question=question_data.question,
        pattern=question_data.pattern,
        imagePath=question_data.image_path,
        ordinal=question_data.ordinal,
        listAnswer=answer_result,
        message="Question updated successfully"
    )


async def delete_question(question_crud: QuestionCRUD, answer_crud: AnswerCRUD,
                          question_id: int) -> QuestionDeleteResponse or QuestionWithListAnswerDeleteResponse:
    question_data = question_crud.fetch_question_by_id(question_id)

    if not question_data:
        return QuestionDeleteResponse(
            questionId=question_id,
            message=f"Question with ID {question_id} not found"
        )

    answers = answer_crud.fetch_answer_by_question_id(question_id)

    for answer in answers:
        is_success = answer_crud.delete_answer(answer.answer_id)
        if not is_success:
            return QuestionDeleteResponse(
                questionId=question_id,
                message=f"Failed to delete the answer with ID {answer.answer_id}"
            )

    if question_data.image_path:
        is_success = await s3.remove_file_from_s3(question_data.image_path)
        if not is_success:
            return QuestionDeleteResponse(
                questionId=question_id,
                message="Failed to delete the image"
            )

    is_success = question_crud.delete_question(question_data.question_id)

    if not is_success:
        return QuestionDeleteResponse(
            questionId=question_id,
            message="Failed to delete the question"
        )

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


def create_update_delete_answer(answer_crud: AnswerCRUD, question_id: int,
                                answers: AnswerCreateUpdateDelete) -> AnswerCreateUpdateDeleteBulkResponse:
    success_model = AnswerCreateUpdateDeleteSuccessResponse(create=[], update=[], delete=[])
    failed_model = AnswerCreateUpdateDeleteFailedResponse(create=[], update=[], delete=[])

    answer_result = AnswerCreateUpdateDeleteBulkResponse(success=success_model, failed=failed_model)

    for answer in answers.createUpdate:
        if not answer.answerId:
            result = create_answer(answer_crud, question_id, answer)
            if isinstance(result, AnswerResponse):
                answer_result.success.create.append(result)
            else:
                answer_result.failed.create.append(result)
        else:
            result = update_answer(answer_crud, answer)
            if isinstance(result, AnswerResponse):
                answer_result.success.update.append(result)
            else:
                answer_result.failed.update.append(result)

    for answer in answers.delete:
        is_success = delete_answer(answer_crud, answer.answerId)
        if is_success:
            answer_result.success.delete.append(
                AnswerDeleteResponse(
                    answerId=answer.answerId,
                    message="Answer deleted successfully"
                )
            )
        else:
            answer_result.success.delete.append(
                AnswerDeleteResponse(
                    answerId=answer.answerId,
                    message="Failed to delete the answer"
                )
            )

    return answer_result


def create_answer(answer_crud: AnswerCRUD, question_id: int,
                  answer: AnswerCreateUpdate) -> AnswerCreateFailed or AnswerResponse:
    existed_answers = answer_crud.fetch_answer_by_question_id_and_answer(question_id, answer.answer)
    if existed_answers:
        return AnswerCreateFailed(
            answer=answer.answer,
            message="Answer already exists"
        )

    answer_data = answer_crud.create_answer(question_id, answer.answer, answer.summary, answer.skipToQuestion)

    if answer_data:
        return AnswerResponse(
            answerId=answer_data.answer_id,
            answer=answer_data.answer,
            summary=answer_data.summary,
            skipToQuestion=answer_data.skip_to_question,
            message="Answer added successfully"
        )
    else:
        return AnswerCreateFailed(
            answer=answer.answer,
            message="Failed to add the answer"
        )


def update_answer(answer_crud: AnswerCRUD, answer: AnswerCreateUpdate) -> AnswerUpdateFailed or AnswerResponse:
    existed_answers = answer_crud.fetch_answer_by_id(answer.answerId)
    if not existed_answers:
        return AnswerUpdateFailed(
            answerId=answer.answerId,
            answer=answer.answer,
            summary=answer.summary,
            skipToQuestion=answer.skipToQuestion,
            message="Answer not found"
        )

    answer_data = answer_crud.update_answer(answer.answerId, answer.answer, answer.summary, answer.skipToQuestion)

    if answer_data:
        return AnswerResponse(
            answerId=answer_data.answer_id,
            answer=answer_data.answer,
            summary=answer_data.summary,
            skipToQuestion=answer_data.skip_to_question,
            message="Answer updated successfully"
        )
    else:
        return AnswerUpdateFailed(
            answerId=answer.answerId,
            answer=answer.answer,
            summary=answer.summary,
            skipToQuestion=answer.skipToQuestion,
            message="Failed to update the answer"
        )


def delete_answer(answer_crud: AnswerCRUD, answer_id: int) -> bool:
    return answer_crud.delete_answer(answer_id)


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


@router.get("/test", response_model=QuestionCreateUpdateDelete, tags=["Question"])
async def test():
    return "Hello World"
