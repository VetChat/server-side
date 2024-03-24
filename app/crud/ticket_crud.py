from typing import Optional

from sqlalchemy.orm import Session
from ..models import Ticket, Animal


class TicketCRUD:
    def __init__(self, db: Session):
        self.db = db

    def fetch_tickets(self):
        return self.db.query(Ticket).all()

    def fetch_tickets_id(self, limit: Optional[int] = None, offset: Optional[int] = None):
        query = self.db.query(Ticket.ticket_id).order_by(Ticket.ticket_id.desc())
        query = query.limit(limit)
        query = query.offset(offset)
        return query.all()

    def create_ticket(self, ticket_data):
        animal = self.db.query(Animal).filter(Animal.animal_id == ticket_data.animalId).first()
        # Create a new Ticket instance
        new_ticket = Ticket(
            animal=animal.animal_name,
        )
        self.db.add(new_ticket)
        self.db.commit()
        self.db.refresh(new_ticket)
        return new_ticket

    def fetch_ticket_by_id(self, ticket_id: int):
        return self.db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
