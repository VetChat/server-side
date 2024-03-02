from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base
from datetime import datetime, timezone


class Ticket(Base):
    __tablename__ = 'ticket'

    ticket_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animal.animal_id'), nullable=False)
    sex = Column(Enum('male', 'female'), nullable=False)
    sterilize = Column(Enum('sterile', 'non-sterile'), nullable=False)
    breed = Column(String(255), nullable=False)
    birth_when = Column(DateTime, nullable=False)
    rec_created_when = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    is_answered = Column(Integer, default=0, nullable=False)

    # Relationship to Animal (assuming you have an Animal model defined)
    animal = relationship("Animal")

    def __repr__(self):
        return f"<Ticket(ticket_id={self.ticket_id}, animal_id={self.animal_id}, sex='{self.sex}', " \
               f"sterilize='{self.sterilize}', breed='{self.breed}', birth_when='{self.birth_when}', " \
               f"rec_created_when='{self.rec_created_when}')>"
