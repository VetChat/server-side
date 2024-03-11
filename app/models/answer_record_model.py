from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class AnswerRecord(Base):
    __tablename__ = 'answer_record'

    answer_record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('ticket.ticket_id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('answer.answer_id'), nullable=False)

    # Relationships to Ticket and Answer
    ticket = relationship("Ticket", back_populates="answer_records")
    answers = relationship("Answer", back_populates="answer_records")

    def __repr__(self):
        return (f"<AnswerRecord(answer_record_id={self.answer_record_id}, ticket_id={self.ticket_id}, "
                f"answer_id={self.answer_id})>")
