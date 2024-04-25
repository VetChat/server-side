from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from app.database import Base


class Breed(Base):
    __tablename__ = 'breed'

    breed_id = Column(Integer, primary_key=True, autoincrement=True)
    breed_name = Column(String(255), nullable=False)
    animal_id = Column(Integer, ForeignKey('animal.animal_id', ondelete='CASCADE'), nullable=False)

    animal = relationship('Animal')

    __table_args__ = (UniqueConstraint('breed_name', name='UC_Animal'),)

    def __repr__(self):
        return f"<Breed(breed_id={self.breed_id}, breed_name={self.breed_name}, animal_id={self.animal_id})>"
