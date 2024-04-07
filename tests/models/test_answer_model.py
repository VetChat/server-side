from app.models.answer_model import Answer


def test_answer_creation():
    answer = Answer(answer_id=1, question_id=1, answer="Test Answer", summary="Test Summary", skip_to_question=2)
    assert answer.answer_id == 1
    assert answer.question_id == 1
    assert answer.answer == "Test Answer"
    assert answer.summary == "Test Summary"
    assert answer.skip_to_question == 2


def test_answer_repr():
    answer = Answer(answer_id=1, question_id=1, answer="Test Answer", summary="Test Summary", skip_to_question=2)
    assert repr(
        answer) == "<Answer(answer_id=1, question_id=1, answers='Test Answer', summary='Test Summary', skip_to_question=2)>"


def test_answer_creation_without_optional_fields():
    answer = Answer(answer_id=1, question_id=1, answer="Test Answer")
    assert answer.answer_id == 1
    assert answer.question_id == 1
    assert answer.answer == "Test Answer"
    assert answer.summary is None
    assert answer.skip_to_question is None


def test_answer_repr_without_optional_fields():
    answer = Answer(answer_id=1, question_id=1, answer="Test Answer")
    assert repr(
        answer) == "<Answer(answer_id=1, question_id=1, answers='Test Answer', summary='None', skip_to_question=None)>"
