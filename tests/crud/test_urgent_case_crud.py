from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from app.models import UrgentCase
from app.crud import UrgentCaseCRUD


def test_fetch_all_urgent_case_returns_all_cases():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.fetch_all_urgent_case()
    session.query.assert_called_once_with(UrgentCase)


def test_fetch_urgent_case_by_animal_id_returns_correct_cases():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.fetch_urgent_case_by_animal_id(1)
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()


def test_fetch_urgent_case_by_id_returns_correct_case():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.fetch_urgent_case_by_id(1)
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()


def test_fetch_urgent_case_by_ids_returns_correct_cases():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.fetch_urgent_case_by_ids([1, 2])
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()


def test_fetch_urgent_case_by_name_returns_correct_case():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.fetch_urgent_case_by_name(1, "urgent_name")
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()


def test_fetch_urgent_cases_by_name_returns_correct_cases():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.fetch_urgent_cases_by_name(1, ["urgent_name1", "urgent_name2"])
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()


def test_fetch_urgent_case_with_urgency_detail_returns_correct_cases():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.fetch_urgent_case_with_urgency_detail()
    session.query.assert_called_once_with(UrgentCase)


def test_add_urgent_case_adds_case_to_db():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.add_urgent_case("urgent_name", 1, 1)
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_update_urgent_case_updates_case_in_db():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.update_urgent_case(1, "urgent_name", 1)
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_update_multiple_urgent_cases_updates_cases_in_db():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.update_multiple_urgent_cases([{"urgent_id": 1, "urgent_name": "urgent_name", "urgency_id": 1}])
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_remove_urgent_case_removes_case_from_db():
    session = create_autospec(Session, instance=True)
    crud = UrgentCaseCRUD(session)
    crud.remove_urgent_case(1)
    session.query.assert_called_once_with(UrgentCase)
    session.query().filter.assert_called_once()
    session.delete.assert_called_once()
    session.commit.assert_called_once()
