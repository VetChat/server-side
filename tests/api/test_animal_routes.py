from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch('app.api.animal_routes.get_db')
def test_animals_retrieval(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.all.return_value = []
    response = client.get("/animals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch('app.api.animal_routes.get_db')
def test_animal_retrieval_by_id(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/animal/1")
    assert response.status_code == 404


@patch('app.api.animal_routes.get_db')
def test_animal_addition(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = None
    response = client.post("/animal", json={"animalName": "Lion"})
    assert response.status_code == 200
    assert response.json()["animalName"] == "Lion"


@patch('app.api.animal_routes.get_db')
def test_animal_addition_already_exists(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = True
    response = client.post("/animal", json={"animalName": "Lion"})
    assert response.status_code == 409


@patch('app.api.animal_routes.get_db')
def test_animal_update(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = True
    response = client.put("/animal", json={"animalId": 1, "animalName": "Tiger"})
    assert response.status_code == 200
    assert response.json()["newAnimalName"] == "Tiger"


@patch('app.api.animal_routes.get_db')
def test_animal_update_not_found(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/animal", json={"animalId": 9999, "animalName": "Tiger"})
    assert response.status_code == 404


@patch('app.api.animal_routes.get_db')
def test_animal_removal(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = True
    response = client.delete("/animal/1")
    assert response.status_code == 200


@patch('app.api.animal_routes.get_db')
def test_animal_removal_not_found(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/animal/9999")
    assert response.status_code == 404
