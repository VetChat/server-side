from app.crud import QuestionCRUD
from app.models import Question
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock


def test_question_crud_fetch_by_id_happy_path():
    with patch.object(Session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.filter.return_value.first.return_value = Question(question_id=1)
        crud = QuestionCRUD(Session())
        result = crud.fetch_question_by_id(1)
        assert result.question_id == 1


def test_question_crud_fetch_by_id_no_result():
    with patch.object(Session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.filter.return_value.first.return_value = None
        crud = QuestionCRUD(Session())
        result = crud.fetch_question_by_id(1)
        assert result is None


def test_question_crud_create_question_happy_path():
    with patch.object(Session, 'add', return_value=None) as mock_add, \
            patch.object(Session, 'commit', return_value=None) as mock_commit, \
            patch.object(Session, 'refresh', return_value=None) as mock_refresh:
        crud = QuestionCRUD(Session())
        result = crud.create_question(1, 'question', 'pattern', 1)
        assert result is not None


def test_question_crud_create_question_db_error():
    with patch.object(Session, 'add', return_value=None) as mock_add, \
            patch.object(Session, 'commit', side_effect=Exception()) as mock_commit, \
            patch.object(Session, 'rollback', return_value=None) as mock_rollback:
        crud = QuestionCRUD(Session())
        result = crud.create_question(1, 'question', 'pattern', 1)
        assert result is None


def test_question_crud_delete_question_happy_path():
    with patch.object(Session, 'delete', return_value=None) as mock_delete, \
            patch.object(Session, 'commit', return_value=None) as mock_commit:
        crud = QuestionCRUD(Session())
        result = crud.delete_question(1)
        assert result is True


def test_question_crud_delete_question_no_result():
    with patch.object(Session, 'delete', return_value=None) as mock_delete, \
            patch.object(Session, 'commit', return_value=None) as mock_commit:
        crud = QuestionCRUD(Session())
        result = crud.delete_question(1)
        assert result is False
