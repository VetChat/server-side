from collections import defaultdict
from typing import Optional

from fastapi import Request, APIRouter, Depends
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from app.crud import TicketCRUD, SummaryCRUD
from app.database import get_db
from app.schemas import TicketSummaryResponse, TicketInfo, SymptomSummary, AnswerSummary, TicketLabel, \
    TicketEachSummaryResponse, TicketDataResponse
from app.utils import limiter


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(generate_unique_id_function=custom_generate_unique_id)


@router.get("/summary", response_model=TicketSummaryResponse, tags=["Summary"])
@limiter.limit("20/minute")
async def get_summary(request: Request, limit: Optional[int] = 50, start_at: Optional[int] = 0,
                      db: Session = Depends(get_db)) -> TicketSummaryResponse:
    ticket_crud = TicketCRUD(db)
    tickets_id = {ticket_id.ticket_id: ticket_id.rec_created_when for ticket_id in
                  ticket_crud.fetch_tickets_id(limit, start_at)}

    summary_crud = SummaryCRUD(db)

    ticket_info = summary_crud.fetch_ticket_info_by_ticket_ids(tickets_id)
    fifth_question = summary_crud.fetch_ticket_questions_by_range(5)
    summary = summary_crud.fetch_summary_by_ticket_ids(tickets_id)

    dict_ticket_info = {ticket_id: [] for ticket_id in tickets_id}
    dict_summary = {ticket_id: {} for ticket_id in tickets_id}

    for each in ticket_info:
        dict_ticket_info[each.ticket_id].append(each)

    for each in summary:
        dict_summary[each.ticket_id].setdefault(each.symptom_id, []).append(each)

    return TicketSummaryResponse(
        label=[
            TicketLabel(
                ticketQuestion=label.ticket_question,
                ordinal=label.ordinal
            ) for label in fifth_question
        ],
        listTicket=[
            TicketDataResponse(
                ticketId=ticket_id,
                recCreatedWhen=tickets_id[ticket_id],
                info=[
                    TicketInfo(
                        ticketAnswerRecordId=info.ticket_answer_record_id,
                        ticketAnswer=info.ticket_answer,
                        ticketQuestion=info.ticket_question,
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
                                question=answer.question,
                                imagePath=answer.image_path,
                                ordinal=i,
                                answer=answer.answer,
                                summary=answer.summary
                            ) for i, answer in enumerate(dict_summary[ticket_id][symptom_id], start=1)
                        ]
                    ) for symptom_id in dict_summary[ticket_id]
                ]
            ) for ticket_id in tickets_id
        ]
    )


@router.get("/summary/{ticket_id}", response_model=TicketEachSummaryResponse, tags=["Summary"])
@limiter.limit("20/minute")
async def get_summary_by_ticket_id(request: Request, ticket_id: int,
                                   db: Session = Depends(get_db)) -> TicketEachSummaryResponse:
    summary_crud = SummaryCRUD(db)

    ticket_info = summary_crud.fetch_ticket_info_by_ticket_id(ticket_id)
    summary = summary_crud.fetch_summary_by_ticket_id(ticket_id)

    # Group questions by symptom
    symptom_groups = defaultdict(list)

    for item in summary:
        symptom_groups[(item.symptom_id, item.symptom_name)].append(item)

    return TicketEachSummaryResponse(
        ticketId=ticket_id,
        info=[
            TicketInfo(
                ticketAnswerRecordId=info.ticket_answer_record_id,
                ticketAnswer=info.ticket_answer,
                ticketQuestion=info.ticket_question,
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
                        question=answer.question,
                        imagePath=answer.image_path,
                        ordinal=i,
                        answer=answer.answer,
                        summary=answer.summary
                    ) for i, answer in enumerate(summary, start=1)
                ]
            ) for (symptom_id, symptom_name), summary in symptom_groups.items()
        ]
    )
