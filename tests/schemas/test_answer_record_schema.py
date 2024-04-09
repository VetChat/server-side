import pytest
from pydantic import ValidationError
from app.schemas import answer_record_schema


def test_should_create_answer_record_id_model_successfully():
    answer_record_id = answer_record_schema.AnswerRecordId(questionId=1, answer="Yes")
    assert answer_record_id.questionId == 1
    assert answer_record_id.answer == "Yes"


def test_should_raise_error_when_missing_required_fields_in_answer_record_id_model():
    with pytest.raises(ValidationError):
        answer_record_schema.AnswerRecordId()


def test_should_create_answer_record_create_model_successfully():
    answer_record_create = answer_record_schema.AnswerRecordCreate(ticketId=1, listAnswer=[
        answer_record_schema.AnswerRecordId(questionId=1, answer="Yes")])
    assert answer_record_create.ticketId == 1
    assert answer_record_create.listAnswer[0].questionId == 1
    assert answer_record_create.listAnswer[0].answer == "Yes"


def test_should_raise_error_when_missing_required_fields_in_answer_record_create_model():
    with pytest.raises(ValidationError):
        answer_record_schema.AnswerRecordCreate()


def test_should_create_answer_record_response_model_successfully():
    answer_record_response = answer_record_schema.AnswerRecordResponse(ticketId=1, message="Success")
    assert answer_record_response.ticketId == 1
    assert answer_record_response.message == "Success"


def test_should_raise_error_when_missing_required_fields_in_answer_record_response_model():
    with pytest.raises(ValidationError):
        answer_record_schema.AnswerRecordResponse()
