from typing import List
from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils import limiter
from ..database import get_db
from ..crud import TicketQuestionCRUD
from ..schemas import TicketQuestionRead, TicketAnswerRead

router = APIRouter()


@router.get("/ticket_questions", response_model=List[TicketQuestionRead], tags=["Ticket Questions"])
@limiter.limit("10/minute")
async def get_ticket_questions(request: Request, db: Session = Depends(get_db)) -> List[TicketQuestionRead]:
    ticket_question_crud = TicketQuestionCRUD(db)
    questions = ticket_question_crud.fetch_ticket_questions_with_answers()

    questions_response = [
        TicketQuestionRead(
            questionId=question.ticket_question_id,
            question=question.ticket_question,
            pattern=question.pattern,
            ordinal=question.ordinal,
            isRequired=question.is_required,
            listAnswer=[
                TicketAnswerRead(
                    answerId=answer.ticket_answer_id,
                    answer=answer.ticket_answer
                )
                for answer in question.ticket_answers
            ]
        )
        for question in questions
    ]

    return questions_response
