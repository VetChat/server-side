import pytest
from pydantic import ValidationError
from app.schemas import animal_schema


def test_should_create_animal_read_model_successfully():
    animal_read = animal_schema.AnimalRead(animalId=1, animalName="Dog")
    assert animal_read.animalId == 1
    assert animal_read.animalName == "Dog"


def test_should_raise_error_when_missing_required_fields_in_animal_read_model():
    with pytest.raises(ValidationError):
        animal_schema.AnimalRead()


def test_should_create_animal_create_model_successfully():
    animal_create = animal_schema.AnimalCreate(animalName="Cat")
    assert animal_create.animalName == "Cat"


def test_should_raise_error_when_missing_required_fields_in_animal_create_model():
    with pytest.raises(ValidationError):
        animal_schema.AnimalCreate()


def test_should_create_animal_response_model_successfully():
    animal_response = animal_schema.AnimalResponse(animalId=2, animalName="Bird", message="Success")
    assert animal_response.animalId == 2
    assert animal_response.animalName == "Bird"
    assert animal_response.message == "Success"


def test_should_raise_error_when_missing_required_fields_in_animal_response_model():
    with pytest.raises(ValidationError):
        animal_schema.AnimalResponse()


def test_should_create_animal_update_model_successfully():
    animal_update = animal_schema.AnimalUpdate(animalId=3, oldAnimalName="Fish", newAnimalName="Shark",
                                               message="Updated")
    assert animal_update.animalId == 3
    assert animal_update.oldAnimalName == "Fish"
    assert animal_update.newAnimalName == "Shark"
    assert animal_update.message == "Updated"


def test_should_raise_error_when_missing_required_fields_in_animal_update_model():
    with pytest.raises(ValidationError):
        animal_schema.AnimalUpdate()
