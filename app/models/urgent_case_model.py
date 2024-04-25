from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base


class UrgentCase(Base):
    __tablename__ = 'urgent_case'

    urgent_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    urgent_name = Column(String(255), nullable=False)
    urgency_id = Column(Integer, ForeignKey('urgency.urgency_id'), nullable=False)
    animal_id = Column(Integer, ForeignKey('animal.animal_id', ondelete='CASCADE'), nullable=False)

    # Relationships to Urgency and Animal
    urgency = relationship("Urgency", back_populates="urgent_cases")
    animal = relationship("Animal")  # Assuming you have an Animal model defined

    # Unique constraint on urgent_name and animal_id
    __table_args__ = (UniqueConstraint('urgent_name', 'animal_id', name='UC_Urgent'),)

    def __repr__(self):
        return f"<UrgentCase(urgent_id={self.urgent_id}, urgent_name='{self.urgent_name}', urgency_id={self.urgency_id}, animal_id={self.animal_id})>"
