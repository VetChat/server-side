from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from app.models import Answer
from app.crud import AnswerCRUD


def test_fetch_answer_by_id_returns_correct_answer():
    session = create_autospec(Session, instance=True)
    crud = AnswerCRUD(session)
    crud.fetch_answer_by_id(1)
    session.query.assert_called_once_with(Answer)
    session.query().filter.assert_called_once()


def test_fetch_answer_by_question_id_and_answer_returns_correct_answer():
    session = create_autospec(Session, instance=True)
    crud = AnswerCRUD(session)
    crud.fetch_answer_by_question_id_and_answer(1, "Yes")
    session.query.assert_called_once_with(Answer)
    session.query().filter.assert_called_once()


def test_create_answer_adds_answer_to_db():
    session = create_autospec(Session, instance=True)
    crud = AnswerCRUD(session)
    crud.create_answer(1, "Yes", "Summary", 2)
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_update_answer_updates_answer_in_db():
    session = create_autospec(Session, instance=True)
    crud = AnswerCRUD(session)
    crud.update_answer(1, "No", "Summary", 2)
    session.query.assert_called_once_with(Answer)
    session.query().filter.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_delete_answer_removes_answer_from_db():
    session = create_autospec(Session, instance=True)
    crud = AnswerCRUD(session)
    crud.delete_answer(1)
    session.query.assert_called_once_with(Answer)
    session.query().filter.assert_called_once()
    session.delete.assert_called_once()
    session.commit.assert_called_once()
