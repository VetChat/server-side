from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from app.models import Animal
from app.crud import AnimalCRUD


def test_fetch_all_animal_returns_all_animals():
    session = create_autospec(Session, instance=True)
    crud = AnimalCRUD(session)
    crud.fetch_all_animal()
    session.query.assert_called_once_with(Animal)


def test_fetch_animal_by_id_returns_correct_animal():
    session = create_autospec(Session, instance=True)
    crud = AnimalCRUD(session)
    crud.fetch_animal_by_id(1)
    session.query.assert_called_once_with(Animal)
    session.query().filter.assert_called_once()


def test_fetch_animal_by_name_returns_correct_animal():
    session = create_autospec(Session, instance=True)
    crud = AnimalCRUD(session)
    crud.fetch_animal_by_name("Lion")
    session.query.assert_called_once_with(Animal)
    session.query().filter.assert_called_once()


def test_add_animal_adds_animal_to_db():
    session = create_autospec(Session, instance=True)
    crud = AnimalCRUD(session)
    crud.add_animal("Lion")
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_update_animal_updates_animal_in_db():
    session = create_autospec(Session, instance=True)
    crud = AnimalCRUD(session)
    crud.update_animal(1, "Tiger")
    session.query.assert_called_once_with(Animal)
    session.query().filter.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_remove_animal_removes_animal_from_db():
    session = create_autospec(Session, instance=True)
    crud = AnimalCRUD(session)
    crud.remove_animal(1)
    session.query.assert_called_once_with(Animal)
    session.query().filter.assert_called_once()
    session.delete.assert_called_once()
    session.commit.assert_called_once()
