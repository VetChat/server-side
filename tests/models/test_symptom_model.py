from app.models.symptom_model import Symptom


def test_symptom_creation():
    symptom = Symptom(symptom_id=1, symptom_name="Fever")
    assert symptom.symptom_id == 1
    assert symptom.symptom_name == "Fever"


def test_symptom_repr():
    symptom = Symptom(symptom_id=1, symptom_name="Fever")
    assert repr(symptom) == "<Symptom(symptom_id=1, symptom_name='Fever')>"


def test_symptom_creation_with_same_name():
    symptom1 = Symptom(symptom_id=1, symptom_name="Fever")
    symptom2 = Symptom(symptom_id=2, symptom_name="Fever")
    assert symptom1.symptom_name == symptom2.symptom_name


def test_symptom_repr_with_same_name():
    symptom1 = Symptom(symptom_id=1, symptom_name="Fever")
    symptom2 = Symptom(symptom_id=2, symptom_name="Fever")
    assert repr(symptom1) == repr(symptom2)
