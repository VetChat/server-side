from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class TicketAnswer(Base):
    __tablename__ = 'ticket_answer'

    ticket_answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_question_id = Column(Integer, ForeignKey('ticket_question.ticket_question_id'), nullable=False)
    ticket_answer = Column(String(255), nullable=False)

    # Relationship to TicketQuestion
    ticket_question = relationship("TicketQuestion", back_populates="ticket_answers")

    def __repr__(self):
        return f"<TicketAnswer(ticket_answer_id={self.ticket_answer_id}, " \
               f"ticket_question_id={self.ticket_question_id}, ticket_answer='{self.ticket_answer}')>"
