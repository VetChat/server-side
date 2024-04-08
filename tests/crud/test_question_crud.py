from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from app.models import Question
from app.crud import QuestionCRUD


def test_fetch_question_by_question_and_question_set_id_returns_correct_question():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.fetch_question_by_question_and_question_set_id("question", 1)
    session.query.assert_called_once_with(Question.question_id, Question.question)
    session.query().filter.assert_called_once()


def test_fetch_questions_by_questions_and_question_set_id_returns_correct_questions():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.fetch_questions_by_questions_and_question_set_id(["question1", "question2"], 1)
    session.query.assert_called_once_with(Question)
    session.query().filter.assert_called_once()


def test_fetch_question_by_id_returns_correct_question():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.fetch_question_by_id(1)
    session.query.assert_called_once_with(Question)
    session.query().filter.assert_called_once()


def test_fetch_question_by_list_id_returns_correct_questions():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.fetch_question_by_list_id([1, 2])
    session.query.assert_called_once_with(Question)
    session.query().filter.assert_called_once()


def test_fetch_questions_by_question_set_id_returns_correct_questions():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.fetch_questions_by_question_set_id(1)
    session.query.assert_called_once_with(Question)
    session.query().filter.assert_called_once()


def test_fetch_questions_by_set_ids_returns_correct_questions():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.fetch_questions_by_set_ids([1, 2])
    session.query.assert_called_once_with(Question)
    session.query().filter.assert_called_once()


def test_create_question_adds_question_to_db():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.create_question(1, 'question', 'pattern', 1)
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_update_question_updates_question_in_db():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.update_question(1, 'question', 'pattern', 1)
    session.query.assert_called_once_with(Question)
    session.query().filter.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_delete_question_removes_question_from_db():
    session = create_autospec(Session, instance=True)
    crud = QuestionCRUD(session)
    crud.delete_question(1)
    session.query.assert_called_once_with(Question)
    session.query().filter.assert_called_once()
    session.delete.assert_called_once()
    session.commit.assert_called_once()
