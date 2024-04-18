from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class TicketQuestion(Base):
    __tablename__ = 'ticket_question'

    ticket_question_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_question = Column(String(255), nullable=False)
    pattern = Column(Enum('text', 'choice', 'birthDate', 'breed'), nullable=False)
    ordinal = Column(Integer, nullable=False)
    is_required = Column(Boolean, nullable=False, default=True)
    is_default = Column(Boolean, nullable=False, default=False)

    # Relationship to TicketAnswer
    ticket_answers = relationship("TicketAnswer", back_populates="ticket_question")

    def __repr__(self):
        return f"<TicketQuestion(ticket_question_id={self.ticket_question_id}, " \
               f"ticket_question='{self.ticket_question}', pattern='{self.pattern}', ordinal={self.ordinal}, " \
               f"is_required={self.is_required})>"
