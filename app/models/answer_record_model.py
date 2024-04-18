from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base


class AnswerRecord(Base):
    __tablename__ = 'answer_record'

    answer_record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('ticket.ticket_id', ondelete='CASCADE'), nullable=False)
    symptom_id = Column(Integer, nullable=False)
    symptom_name = Column(String(255), nullable=False)
    question = Column(String(255), nullable=False)
    image_path = Column(String(255))
    ordinal = Column(Integer, nullable=False)
    answer = Column(String(255), nullable=False)
    summary = Column(String(255))

    # Relationships to Ticket and Answer
    ticket = relationship("Ticket", back_populates="answer_records")

    __table_args__ = (UniqueConstraint('ticket_id', 'question', name='UC_AnswerTicket'),)

    def __repr__(self):
        return f"<AnswerRecord(answer_record_id={self.answer_record_id}, ticket_id={self.ticket_id}, " \
               f"question='{self.question}', answer='{self.answer}', summary='{self.summary}')>"
