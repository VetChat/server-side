import pytest
from unittest.mock import patch

from app.api.animal_routes import get_animal  # Import the function to be tested
from app.schemas import AnimalRead  # Import schemas for assertions


@pytest.fixture
def mock_db_session():
    # Mock database session with sample data
    with patch("app.database.get_db") as mock_db:
        mock_animals = [
            {"animal_id": 1, "animal_name": "Lion"},
            {"animal_id": 2, "animal_name": "Tiger"},
        ]
        mock_db.return_value.query().all.return_value = mock_animals
        yield mock_db


def test_get_animals_success(mock_db_session):
    response = get_animal()
    assert response == [
        AnimalRead(animalId=1, animalName="Lion"),
        AnimalRead(animalId=2, animalName="Tiger"),
    ]
