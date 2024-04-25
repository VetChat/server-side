from typing import Type, List, Optional
from sqlalchemy.orm import Session
from app.models import Breed


class BreedCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def fetch_breed_by_id(self, breed_id: int) -> Optional[Type[Breed]]:
        return self.db.query(Breed).filter(Breed.breed_id == breed_id).first()

    def fetch_breed_by_name(self, breed_name: str) -> Optional[Type[Breed]]:
        return self.db.query(Breed).filter(Breed.breed_name == breed_name).first()

    def fetch_breed_by_animal_id(self, animal_id: int) -> List[Type[Breed]]:
        return self.db.query(Breed).filter(Breed.animal_id == animal_id).all()

    def add_breed(self, animal_id: int, breed_name: str) -> Breed:
        new_breed = Breed(
            animal_id=animal_id,
            breed_name=breed_name
        )
        self.db.add(new_breed)
        self.db.commit()
        self.db.refresh(new_breed)
        return new_breed

    def update_breed(self, breed_id: int, breed_name: str) -> Optional[Type[Breed]]:
        breed = self.fetch_breed_by_id(breed_id)
        if breed:
            breed.breed_name = breed_name
            self.db.commit()
            self.db.refresh(breed)
            return breed
        return None

    def remove_breed(self, breed_id: int) -> bool:
        breed = self.db.query(Breed).filter(Breed.breed_id == breed_id).first()
        if breed:
            self.db.delete(breed)
            self.db.commit()
            return True
        return False
