from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routers

app = FastAPI()

for route in routers:
    app.include_router(route)

origins = [
    "http://localhost:3000",  # Local frontend development server
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
async def read_root():
    # Perform a database operation here if needed
    return {"Hello": "World"}
