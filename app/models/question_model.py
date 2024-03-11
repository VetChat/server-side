from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Question(Base):
    __tablename__ = 'question'

    question_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_set_id = Column(Integer, ForeignKey('question_set.question_set_id'), nullable=False)
    question = Column(String(255), nullable=False)
    pattern = Column(Enum('choice', 'yes/no', 'duration'), nullable=False)
    image_path = Column(String(255))
    ordinal = Column(Integer, nullable=False)

    # Relationship to QuestionSet
    question_set = relationship("QuestionSet", back_populates="questions")
    # Relationship to Answer
    answers = relationship("Answer", back_populates="question", order_by="Answer.answer_id")

    def __repr__(self):
        return f"<Question(question_id={self.question_id}, question_set_id={self.question_set_id}, " \
               f"question='{self.question}', pattern='{self.pattern}', image_path='{self.image_path}', " \
               f"ordinal={self.ordinal})>"
