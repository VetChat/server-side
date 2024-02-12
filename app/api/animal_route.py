from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import fetch_animal
from ..schemas import AnimalRead

router = APIRouter()


@router.get(f"/animals", response_model=AnimalRead)
def fetch_pet(db: Session = Depends(get_db)) -> List[AnimalRead]:
    return fetch_pet(fetch_animal(db=db))
