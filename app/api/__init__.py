from .summary_routes import router as summary_router
from .animal_routes import router as animal_router
from .urgent_case_routes import router as urgent_router
from .urgency_routes import router as urgency_router
from .ticket_routes import router as ticket_router
from .question_routes import router as question_router
from .answer_record_routes import router as answer_record_router
from .ticket_question_routes import router as ticket_question_router
from .symptom_routes import router as symptom_router

routers = [animal_router, urgent_router, urgency_router, ticket_router, question_router, answer_record_router,
           ticket_question_router, symptom_router, summary_router]

__all__ = ["routers"]
