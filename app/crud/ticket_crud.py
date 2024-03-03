from sqlalchemy.orm import Session
from ..models import Ticket


class TicketCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_ticket(self, ticket_data):
        # Create a new Ticket instance
        new_ticket = Ticket(
            animal_id=ticket_data.animalId,
            sex=ticket_data.sex,
            sterilize=ticket_data.sterilize,
            breed=ticket_data.breed,
            birth_when=ticket_data.birthWhen
        )
        self.db.add(new_ticket)
        self.db.commit()
        self.db.refresh(new_ticket)
        return new_ticket

    def fetch_ticket_by_id(self, ticket_id: int):
        return self.db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
