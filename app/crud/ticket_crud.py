from sqlalchemy.orm import Session
from ..models import Ticket


class TicketCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_ticket(self, ticket_data):
        # Create a new Ticket instance
        new_ticket = Ticket(**ticket_data.dict())
        self.db.add(new_ticket)
        self.db.commit()
        self.db.refresh(new_ticket)
        return new_ticket

    def get_ticket_by_id(self, ticket_id: int):
        return self.db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
