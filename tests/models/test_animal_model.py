import pytest
from unittest.mock import MagicMock, create_autospec
from sqlalchemy.exc import IntegrityError
from app.models import Animal


def test_create_animal_success():
    session = MagicMock()
    new_animal = create_autospec(Animal, instance=True)
    new_animal.animal_name = "Lion"
    session.add(new_animal)
    session.commit()
    assert new_animal.animal_id is not None
    assert new_animal.animal_name == "Lion"
    session.close.assert_called_once()


def test_create_animal_without_name():
    session = MagicMock()
    new_animal = create_autospec(Animal, instance=True)
    session.add(new_animal)
    session.commit.side_effect = IntegrityError(None, None, None)
    with pytest.raises(IntegrityError):
        session.commit()
    session.close.assert_called_once()


def test_create_animal_duplicate_name():
    session = MagicMock()
    new_animal1 = create_autospec(Animal, instance=True)
    new_animal1.animal_name = "Tiger"
    new_animal2 = create_autospec(Animal, instance=True)
    new_animal2.animal_name = "Tiger"
    session.add(new_animal1)
    session.add(new_animal2)
    session.commit.side_effect = IntegrityError(None, None, None)
    with pytest.raises(IntegrityError):
        session.commit()
    session.close.assert_called_once()
