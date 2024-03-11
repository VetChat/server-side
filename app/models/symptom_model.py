from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..database import Base


class Symptom(Base):
    __tablename__ = 'symptom'

    symptom_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symptom_name = Column(String(255), nullable=False, unique=True)

    __table_args__ = (UniqueConstraint('symptom_name', name='UC_Symptom'),)

    def __repr__(self):
        return f"<Symptom(symptom_id={self.symptom_id}, symptom_name='{self.symptom_name}')>"
