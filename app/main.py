from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    # Perform a database operation here if needed
    return {"Hello": "World"}
