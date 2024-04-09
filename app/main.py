from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .utils import limiter
from .api import routers

app = FastAPI(docs_url=None)

# Add the rate limit exceeded error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

for route in routers:
    app.include_router(route)

origins = [
    "http://localhost:5173",  # Local frontend development server
    "https://example.com",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@limiter.limit("5/minute")
async def read_root(request: Request):
    return {"Hello": "World"}
