from .animal_routes import router as animal_router
from .urgent_case_routes import router as urgent_router
from .urgency_routes import router as urgency_router
from .ticket_routes import router as ticket_router
from .question_routes import router as question_router

routers = [animal_router, urgent_router, urgency_router, ticket_router, question_router]

__all__ = ["routers"]
