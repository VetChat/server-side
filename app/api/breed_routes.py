from typing import List
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from app.utils import limiter
from app.database import get_db
from app.crud import BreedCRUD
from app.schemas import BreedRead, BreedCreate, BreedCreateUpdateResponse, BreedUpdate


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(generate_unique_id_function=custom_generate_unique_id)


@router.get("/animal/{animal_id}/breeds", response_model=List[BreedRead], tags=["Breeds"])
@limiter.limit("20/minute")
async def get_breed_by_animal_id(request: Request, animal_id: int, db: Session = Depends(get_db)) -> List[BreedRead]:
    breed_crud = BreedCRUD(db)
    breed_data = breed_crud.fetch_breed_by_animal_id(animal_id)
    breed_response = [
        BreedRead(
            breedId=breed.breed_id,
            breedName=breed.breed_name,
        ) for breed in breed_data
    ]
    return breed_response


@router.post("/animal/breed", response_model=BreedCreateUpdateResponse, tags=["Breeds"])
@limiter.limit("10/minute")
async def add_breed(request: Request, breed: BreedCreate, db: Session = Depends(get_db)) -> BreedCreateUpdateResponse:
    breed_crud = BreedCRUD(db)

    if breed_crud.fetch_breed_by_name(breed.breedName):
        raise HTTPException(status_code=409, detail=f"Breed with name {breed.breedName} already exists")

    breed_data = breed_crud.add_breed(breed.animalId, breed.breedName)
    return BreedCreateUpdateResponse(
        breedId=breed_data.breed_id,
        breedName=breed_data.breed_name,
        animalId=breed_data.animal_id,
        message="The breed has been successfully added."
    )


@router.put("/animal/breed", response_model=BreedCreateUpdateResponse, tags=["Breeds"])
@limiter.limit("5/minute")
async def update_breed(request: Request, breed: BreedUpdate,
                       db: Session = Depends(get_db)) -> BreedCreateUpdateResponse:
    breed_crud = BreedCRUD(db)
    existing_breed = breed_crud.fetch_breed_by_id(breed.breedId)
    if existing_breed is None:
        raise HTTPException(status_code=404, detail=f"Breed with id {breed.breedId} not found")

    breed_data = breed_crud.update_breed(breed.breedId, breed.breedName)
    if breed_data is None:
        raise HTTPException(status_code=500, detail=f"Failed to update the breed id: {breed.breedId}")

    return BreedCreateUpdateResponse(
        breedId=breed_data.breed_id,
        breedName=breed_data.breed_name,
        animalId=breed_data.animal_id,
        message="The breed has been successfully updated."
    )


@router.delete("/animal/breed/{breed_id}", response_model=BreedCreateUpdateResponse, tags=["Breeds"])
@limiter.limit("5/minute")
async def remove_breed(request: Request, breed_id: int, db: Session = Depends(get_db)) -> BreedCreateUpdateResponse:
    breed_crud = BreedCRUD(db)
    breed_data = breed_crud.fetch_breed_by_id(breed_id)
    if breed_data is None:
        raise HTTPException(status_code=404, detail=f"Breed with id {breed_id} not found")

    is_success = breed_crud.remove_breed(breed_id)
    if not is_success:
        raise HTTPException(status_code=500, detail=f"Failed to remove the breed id: {breed_id}")

    return BreedCreateUpdateResponse(
        breedId=breed_data.breed_id,
        breedName=breed_data.breed_name,
        animalId=breed_data.animal_id,
        message="The breed has been successfully removed."
    )
