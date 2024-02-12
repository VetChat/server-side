from typing import Type, List
from sqlalchemy.orm import Session
from ..models import Animal
from ..schemas import AnimalRead


def fetch_animal(db: Session):
    return db.query(Animal).all()


def fetch_animal_by_id(db: Session, animal_id: int) -> Type[AnimalRead] | None:
    return db.query(Animal).filter(Animal.id == animal_id).first()
