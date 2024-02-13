from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base


class QuestionSet(Base):
    __tablename__ = 'question_set'

    question_set_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symptom_id = Column(Integer, ForeignKey('symptom.symptom_id'), nullable=False)
    animal_id = Column(Integer, ForeignKey('animal.animal_id'), nullable=False)

    # Relationships to Symptom and Animal
    symptom = relationship("Symptom")
    animal = relationship("Animal")

    def __repr__(self):
        return f"<QuestionSet(question_set_id={self.question_set_id}, symptom_id={self.symptom_id}, animal_id={self.animal_id})>"
