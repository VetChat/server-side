from typing import Type, List, Optional
from sqlalchemy.orm import Session
from app.models import Animal


class AnimalCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_all_animal(self) -> List[Type[Animal]]:
        return self.db.query(Animal).all()

    def fetch_animal_by_id(self, animal_id: int) -> Optional[Type[Animal]]:
        return (self.db.query(Animal)
                .filter(Animal.animal_id == animal_id)
                .first())

    def fetch_animal_by_name(self, animal_name: str) -> Optional[Type[Animal]]:
        return self.db.query(Animal).filter(Animal.animal_name == animal_name).first()

    def add_animal(self, animal_name: str) -> Animal:
        new_animal = Animal(
            animal_name=animal_name
        )
        self.db.add(new_animal)
        self.db.commit()
        self.db.refresh(new_animal)
        return new_animal

    def update_animal(self, animal_id: int, animal_name: str) -> Optional[Type[Animal]]:
        animal = self.fetch_animal_by_id(animal_id)
        if animal:
            animal.animal_name = animal_name
            self.db.commit()
            self.db.refresh(animal)
            return animal
        return None

    def remove_animal(self, animal_id: int) -> bool:
        animal = self.fetch_animal_by_id(animal_id)
        if animal:
            self.db.delete(animal)
            self.db.commit()
            return True
        return False
