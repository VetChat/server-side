from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timezone


class Ticket(Base):
    __tablename__ = 'ticket'

    ticket_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    animal = Column(String(255), nullable=False)
    rec_created_when = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    is_answered = Column(Boolean, default=False, nullable=False)

    # Relationship to AnswerRecord
    answer_records = relationship("AnswerRecord", back_populates="ticket")
    # Relationship to TicketAnswerRecord
    ticket_answer_records = relationship("TicketAnswerRecord", back_populates="ticket")

    def __repr__(self):
        return f"<Ticket(ticket_id={self.ticket_id}, animal_id={self.animal_id}, " \
               f"rec_created_when='{self.rec_created_when}', is_answered={self.is_answered})>"
