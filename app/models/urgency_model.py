from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Urgency(Base):
    __tablename__ = 'urgency'

    urgency_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    urgency_detail = Column(String(255), nullable=False, unique=True)
    duration = Column(String(255), nullable=False, unique=True)

    # Relationship to UrgentCase
    urgent_cases = relationship("UrgentCase", back_populates="urgency")

    def __repr__(self):
        return f"<Urgency(urgency_id={self.urgency_id}, urgency_detail='{self.urgency_detail}', duration='{self.duration}')>"
