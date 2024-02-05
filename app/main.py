from typing import List, Dict

import mysql.connector
import os
from fastapi import FastAPI
from urllib.parse import urlparse

from mysql.connector import Error

app = FastAPI()

# Retrieve the database URL from the environment variable
database_url = os.getenv("DATABASE_URL")
parsed_url = urlparse(database_url)

# Extract the connection details
db_config = {
    'user': parsed_url.username,
    'password': parsed_url.password,
    'host': parsed_url.hostname,
    'database': parsed_url.path.lstrip('/'),  # Remove the leading slash
}

# Database connection
try:
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor(dictionary=True)
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    cursor = None


@app.on_event("startup")
async def startup():
    if db_connection.is_connected():
        print("MySQL database connection is open.")


@app.on_event("shutdown")
async def shutdown():
    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("MySQL database connection is closed.")


@app.get("/items")
async def read_items():
    if cursor:
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        return items
    else:
        return {"error": "Database connection is not established"}


@app.get("/")
async def read_root():
    # Perform a database operation here if needed
    return {"Hello": "World"}
