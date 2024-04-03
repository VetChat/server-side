from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..database import Base


class Animal(Base):
    __tablename__ = 'animal'

    animal_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    animal_name = Column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint('animal_name', name='UC_Animal'),)

    def __repr__(self):
        return f"<Animal(animal_id={self.animal_id}, name='{self.animal_name}')>"
