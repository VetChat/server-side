from typing import Type, List
from sqlalchemy.orm import Session
from ..models import Animal


def fetch_animal(db: Session) -> List[Type[Animal]]:
    return db.query(Animal).all()


def fetch_animal_by_id(db: Session, animal_id: int) -> Type[Animal]:
    return db.query(Animal).filter(Animal.id == animal_id).first()
