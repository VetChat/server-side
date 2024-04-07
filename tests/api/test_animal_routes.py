from unittest.mock import MagicMock
from app.api.animal_routes import get_animal_by_id
from app.database import get_db
from app.crud import AnimalCRUD
from app.schemas import AnimalRead


def test_get_animal_by_id(mocker):
    # Arrange
    test_animal_id = 1
    test_animal_name = "Dog"
    mock_animal = AnimalRead(animalId=test_animal_id, animalName=test_animal_name)
    mock_crud = MagicMock(spec=AnimalCRUD)
    mock_crud.fetch_animal_by_id.return_value = mock_animal
    mock_db = mocker.patch.object(get_db, 'return_value', autospec=True)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_animal

    # Act
    response = get_animal_by_id(None, test_animal_id, db=mock_db)

    # Assert
    assert response == mock_animal
    mock_crud.fetch_animal_by_id.assert_called_once_with(test_animal_id)
