from .animal_route import router as animal_router
from .urgent_routes import router as urgent_router

routers = [animal_router, urgent_router]

__all__ = ["routers"]
