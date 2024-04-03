from collections import defaultdict
from typing import Optional, List

from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import TicketCRUD, SummaryCRUD
from app.database import get_db
from app.schemas import TicketSummaryResponse, TicketInfo, SymptomSummary, AnswerSummary
from app.utils import limiter

router = APIRouter()


@router.get("/summary", response_model=List[TicketSummaryResponse], tags=["Summary"])
@limiter.limit("20/minute")
async def get_summary(request: Request, limit: Optional[int] = 50, start_at: Optional[int] = 0,
                      db: Session = Depends(get_db)) -> List[TicketSummaryResponse]:
    ticket_crud = TicketCRUD(db)
    tickets_id = [ticket_id[0] for ticket_id in ticket_crud.fetch_tickets_id(limit, start_at)]

    summary_crud = SummaryCRUD(db)

    ticket_info = summary_crud.fetch_ticket_info_by_ticket_ids(tickets_id)
    summary = summary_crud.fetch_summary_by_ticket_ids(tickets_id)

    dict_ticket_info = {ticket_id: [] for ticket_id in tickets_id}
    dict_summary = {ticket_id: {} for ticket_id in tickets_id}

    for each in ticket_info:
        dict_ticket_info[each.ticket_id].append(each)

    for each in summary:
        dict_summary[each.ticket_id].setdefault(each.symptom_id, []).append(each)

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
        ) for ticket_id in tickets_id
    ]

    return response


@router.get("/summary/{ticket_id}", response_model=TicketSummaryResponse, tags=["Summary"])
@limiter.limit("20/minute")
async def get_summary_by_ticket_id(request: Request, ticket_id: int,
                                   db: Session = Depends(get_db)) -> TicketSummaryResponse:
    summary_crud = SummaryCRUD(db)

    ticket_info = summary_crud.fetch_ticket_info_by_ticket_id(ticket_id)
    summary = summary_crud.fetch_summary_by_ticket_id(ticket_id)

    # Group questions by symptom
    symptom_groups = defaultdict(list)

    for item in summary:
        symptom_groups[(item.symptom_id, item.symptom_name)].append(item)

    return TicketSummaryResponse(
        ticketId=ticket_id,
        info=[
            TicketInfo(
                ticketAnswerRecordId=info.ticket_answer_record_id,
                ticketQuestionId=info.ticket_question_id,
                ticketAnswer=info.ticket_answer,
                ticketQuestion=info.ticket_question,
                pattern=info.pattern,
                ordinal=info.ordinal
            ) for info in ticket_info
        ],
        summary=[
            SymptomSummary(
                symptomId=symptom_id,
                symptomName=symptom_name,
                listAnswer=[
                    AnswerSummary(
                        answerRecordId=answer.answer_record_id,
                        questionId=answer.question_id,
                        question=answer.question,
                        ordinal=answer.ordinal,
                        answer_id=answer.answer_id,
                        answer=answer.answer,
                        summary=answer.summary
                    ) for answer in summary
                ]
            ) for (symptom_id, symptom_name), summary in symptom_groups.items()
        ]
    )
