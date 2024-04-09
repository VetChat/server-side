from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from app.models import Symptom, QuestionSet
from app.crud import SymptomCRUD


def test_fetch_symptoms_returns_all_symptoms():
    session = create_autospec(Session, instance=True)
    crud = SymptomCRUD(session)
    crud.fetch_symptoms()
    session.query.assert_called_once_with(Symptom)


def test_fetch_symptom_by_id_returns_correct_symptom():
    session = create_autospec(Session, instance=True)
    crud = SymptomCRUD(session)
    crud.fetch_symptom_by_id(1)
    session.query.assert_called_once_with(Symptom)
    session.query().filter.assert_called_once()


def test_fetch_symptom_by_name_returns_correct_symptom():
    session = create_autospec(Session, instance=True)
    crud = SymptomCRUD(session)
    crud.fetch_symptom_by_name("Symptom Name")
    session.query.assert_called_once_with(Symptom)
    session.query().filter.assert_called_once()


def test_fetch_symptoms_by_animal_id_returns_correct_symptoms():
    session = create_autospec(Session, instance=True)
    crud = SymptomCRUD(session)
    crud.fetch_symptoms_by_animal_id(1)
    session.query.assert_called_once_with(Symptom.symptom_id, Symptom.symptom_name, QuestionSet.question_set_id)
    session.query().join.assert_called_once()
    session.query().filter.assert_called_once()


def test_add_symptom_adds_new_symptom():
    session = create_autospec(Session, instance=True)
    crud = SymptomCRUD(session)
    crud.add_symptom("New Symptom")
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_update_symptom_updates_existing_symptom():
    session = create_autospec(Session, instance=True)
    crud = SymptomCRUD(session)
    crud.update_symptom(1, "Updated Symptom")
    session.query.assert_called_once_with(Symptom)
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_remove_symptom_removes_existing_symptom():
    session = create_autospec(Session, instance=True)
    crud = SymptomCRUD(session)
    crud.remove_symptom(1)
    session.query.assert_called_once_with(Symptom)
    session.query().filter.assert_called_once()
    session.delete.assert_called_once()
    session.commit.assert_called_once()
