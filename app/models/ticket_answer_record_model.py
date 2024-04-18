from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class TicketAnswerRecord(Base):
    __tablename__ = 'ticket_answer_record'

    ticket_answer_record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('ticket.ticket_id', ondelete='CASCADE'), nullable=False)
    ticket_question = Column(String(255), nullable=False)
    ordinal = Column(Integer, nullable=False)
    ticket_answer = Column(String(255), nullable=False)
    is_editable = Column(Boolean, nullable=False, default=True)

    # Relationships to Ticket
    ticket = relationship("Ticket", back_populates="ticket_answer_records")

    __table_args__ = (UniqueConstraint('ticket_id', 'ticket_question', name='UC_TicketAnswerTicket'),)

    def __repr__(self):
        return f"<TicketAnswerRecord(ticket_answer_record_id={self.ticket_answer_record_id}, " \
               f"ticket_id={self.ticket_id}, ticket_question_id={self.ticket_question_id}, " \
               f"ticket_answer='{self.ticket_answer}')>"
