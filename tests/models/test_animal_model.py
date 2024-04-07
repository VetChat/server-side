import pytest
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models import Animal


def test_create_animal_success():
    session = SessionLocal()
    new_animal = Animal(animal_name="Lion")
    session.add(new_animal)
    session.commit()
    assert new_animal.animal_id is not None
    assert new_animal.animal_name == "Lion"
    session.close()


def test_create_animal_without_name():
    session = SessionLocal()
    new_animal = Animal()
    session.add(new_animal)
    with pytest.raises(IntegrityError):
        session.commit()
    session.close()


def test_create_animal_duplicate_name():
    session = SessionLocal()
    new_animal1 = Animal(animal_name="Tiger")
    new_animal2 = Animal(animal_name="Tiger")
    session.add(new_animal1)
    session.add(new_animal2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.close()
