from typing import Union

from pydantic import BaseModel


class TicketAnswerRecordUpdate(BaseModel):
    ticketAnswerRecordId: int
    answer: Union[str, int]


class TicketAnswerRecordUpdateResponse(TicketAnswerRecordUpdate):
    message: str
