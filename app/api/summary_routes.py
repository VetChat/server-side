from typing import Optional, List

from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import TicketCRUD, SummaryCRUD
from app.database import get_db
from app.schemas import TicketSummaryResponse, TicketInfo, SymptomSummary, AnswerSummary
from app.utils import limiter

router = APIRouter()


@router.get("/summary/", response_model=List[TicketSummaryResponse], tags=["Summary"])
@limiter.limit("20/minute")
async def get_summary(request: Request, limit: Optional[int] = 50, start_at: Optional[int] = 0,
                      db: Session = Depends(get_db)) -> List[TicketSummaryResponse]:
    ticket_crud = TicketCRUD(db)
    tickets_id = ticket_crud.fetch_tickets_id(limit, start_at)
    list_ticket_id = [ticket_id[0] for ticket_id in tickets_id]

    summary_crud = SummaryCRUD(db)

    ticket_info = summary_crud.fetch_ticket_info_by_ticket_ids(list_ticket_id)
    summary = summary_crud.fetch_summary_by_ticket_ids(list_ticket_id)

    dict_ticket_info = {}
    dict_summary = {}
    for ticket_id in list_ticket_id:
        dict_ticket_info[ticket_id] = []
        dict_summary[ticket_id] = {}

    for each in ticket_info:
        info = dict_ticket_info[each.ticket_id]
        info.append(each)

    for each in summary:
        if not dict_summary[each.ticket_id].get(each.symptom_id):
            dict_summary[each.ticket_id][each.symptom_id] = []
        answer = dict_summary[each.ticket_id][each.symptom_id]
        answer.append(each)

    response = [
        TicketSummaryResponse(
            ticketId=ticket_id,
            info=[
                TicketInfo(
                    ticketAnswerRecordId=info.ticket_answer_record_id,
                    ticketQuestionId=info.ticket_question_id,
                    ticketAnswer=info.ticket_answer,
                    ticketQuestion=info.ticket_question,
                    pattern=info.pattern,
                    ordinal=info.ordinal
                ) for info in dict_ticket_info[ticket_id]
            ],
            summary=[
                SymptomSummary(
                    symptomId=dict_summary[ticket_id][symptom_id][0].symptom_id,
                    symptomName=dict_summary[ticket_id][symptom_id][0].symptom_name,
                    listAnswer=[
                        AnswerSummary(
                            answerRecordId=answer.answer_record_id,
                            questionId=answer.question_id,
                            question=answer.question,
                            ordinal=answer.ordinal,
                            answer_id=answer.answer_id,
                            answer=answer.answer,
                            summary=answer.summary
                        ) for answer in dict_summary[ticket_id][symptom_id]
                    ]
                ) for symptom_id in dict_summary[ticket_id]
            ]
        ) for ticket_id in list_ticket_id
    ]

    return response
