from .animal_route import router as animal_router
from .urgent_case_routes import router as urgent_router
from .urgency_routes import router as urgency_router

routers = [animal_router, urgent_router, urgency_router]

__all__ = ["routers"]
