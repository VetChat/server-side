from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Answer(Base):
    __tablename__ = 'answer'

    answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('question.question_id'), nullable=False)
    answer = Column(String(255), nullable=False)
    summary = Column(String(255))
    skip_to_question = Column(Integer)

    # Relationship to Question
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer(answer_id={self.answer_id}, question_id={self.question_id}, " \
               f"answers='{self.answer}', summary='{self.summary}', skip_to_question={self.skip_to_question})>"
