from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils import limiter
from ..database import get_db
from ..schemas import SymptomWithQuestions, SymptomRead, SymptomCreateBody, SymptomResponse, SymptomUpdate
from ..crud import QuestionSetCRUD, AnimalCRUD, SymptomCRUD

router = APIRouter()


@router.get("/symptoms", response_model=List[SymptomRead], tags=["Symptoms"])
@limiter.limit("20/minute")
async def get_symptoms(request: Request, db: Session = Depends(get_db)) -> List[SymptomRead]:
    symptom_crud = SymptomCRUD(db)
    symptom_data = symptom_crud.fetch_symptoms()
    symptom_response = [
        SymptomRead(
            symptomId=symptom.symptom_id,
            symptomName=symptom.symptom_name
        )
        for symptom in symptom_data
    ]
    return symptom_response


@router.get("/symptoms/animal/{animal_id}", response_model=List[SymptomWithQuestions], tags=["Symptoms"])
@limiter.limit("10/minute")
async def get_symptoms_by_animal_id(request: Request, animal_id: int, db: Session = Depends(get_db)) -> (
        List)[SymptomWithQuestions]:
    # Retrieve the ticket to get the animal_id
    animal_crud = AnimalCRUD(db)
    animal = animal_crud.fetch_animal_by_id(animal_id)

    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Get list of symptoms by animal_id
    question_set_crud = QuestionSetCRUD(db)
    symptoms_data = question_set_crud.fetch_symptoms_by_animal_id(animal.animal_id)
    symptoms_response: List[SymptomWithQuestions] = [
        SymptomWithQuestions(
            symptomId=symptoms.symptom_id,
            symptomName=symptoms.symptom_name,
            questionSetId=symptoms.question_set_id
        )
        for symptoms in symptoms_data
    ]

    return symptoms_response


@router.post("/symptom", response_model=SymptomResponse, tags=["Symptoms"])
@limiter.limit("5/minute")
async def add_symptom(request: Request, symptom: SymptomCreateBody,
                      db: Session = Depends(get_db)) -> SymptomResponse:
    symptom_crud = SymptomCRUD(db)
    existing_symptom = symptom_crud.fetch_symptom_by_name(symptom.symptomName)
    if existing_symptom:
        raise HTTPException(status_code=409, detail=f"Symptom with name {symptom.symptomName} already exists")

    symptom_data = symptom_crud.add_symptom(symptom.symptomName)

    return SymptomResponse(
        symptomId=symptom_data.symptom_id,
        symptomName=symptom_data.symptom_name,
        message=f"Symptom {symptom_data.symptom_name} added successfully"
    )


@router.put("/symptom/", response_model=SymptomUpdate, tags=["Symptoms"])
@limiter.limit("5/minute")
async def update_symptom(request: Request, symptom: SymptomRead,
                         db: Session = Depends(get_db)) -> SymptomUpdate:
    symptom_crud = SymptomCRUD(db)
    existing_symptom = symptom_crud.fetch_symptom_by_id(symptom.symptomId)
    if existing_symptom is None:
        raise HTTPException(status_code=404, detail=f"Symptom with name {symptom.symptomId} not found")

    symptom_data = symptom_crud.update_symptom(symptom.symptomId, symptom.symptomName)
    if symptom_data is None:
        raise HTTPException(status_code=500, detail=f"Failed to update the symptom id: {symptom.symptomId}")

    return SymptomUpdate(
        symptomId=symptom_data.symptom_id,
        oldSymptomName=existing_symptom.symptom_name,
        newSymptomName=symptom_data.symptom_name,
        message="The symptom has been successfully updated."
    )


@router.delete("/symptom/{symptom_id}", response_model=SymptomResponse, tags=["Symptoms"])
@limiter.limit("5/minute")
async def remove_symptom(request: Request, symptom_id: int, db: Session = Depends(get_db)) -> SymptomResponse:
    symptom_crud = SymptomCRUD(db)
    symptom_data = symptom_crud.fetch_symptom_by_id(symptom_id)
    if symptom_data is None:
        raise HTTPException(status_code=404, detail=f"Symptom with id {symptom_id} not found")

    is_success = symptom_crud.remove_symptom(symptom_id)
    if not is_success:
        raise HTTPException(status_code=500, detail=f"Failed to remove the symptom id: {symptom_id}")

    return SymptomResponse(
        symptomId=symptom_data.symptom_id,
        symptomName=symptom_data.symptom_name,
        message="The symptom has been successfully removed."
    )
