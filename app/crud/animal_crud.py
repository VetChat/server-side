from typing import Type, List, Optional
from sqlalchemy.orm import Session
from ..models import Animal
from ..schemas import AnimalCreate


class AnimalCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_all_animal(self) -> List[Type[Animal]]:
        return self.db.query(Animal).all()

    def fetch_animal_by_id(self, animal_id: int) -> Optional[Animal]:
        return self.db.query(Animal).filter(Animal.animal_id == animal_id).first()

    def fetch_animal_by_name(self, name: str) -> Optional[Animal]:
        return self.db.query(Animal).filter(Animal.name == name).first()

    def add_animal(self, name: str) -> Animal:
        new_animal = Animal(
            name=name
        )
        self.db.add(new_animal)
        self.db.commit()
        self.db.refresh(new_animal)
        return new_animal
