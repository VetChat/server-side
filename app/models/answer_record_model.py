from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from ..database import Base


class AnswerRecord(Base):
    __tablename__ = 'answer_record'

    answer_record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('ticket.ticket_id'), nullable=False)
    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    summary = Column(String(255))

    # Relationships to Ticket and Answer
    ticket = relationship("Ticket", back_populates="answer_records")

    def __repr__(self):
        return f"<AnswerRecord(answer_record_id={self.answer_record_id}, ticket_id={self.ticket_id}, " \
               f"question='{self.question}', answer='{self.answer}', summary='{self.summary}')>"
