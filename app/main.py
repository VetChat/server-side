from fastapi import FastAPI
from .api import routers

app = FastAPI()

for route in routers:
    app.include_router(route)


@app.get("/")
async def read_root():
    # Perform a database operation here if needed
    return {"Hello": "World"}
