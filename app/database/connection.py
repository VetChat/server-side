import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Retrieve the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# If in a testing environment, use an in-memory SQLite database
if os.getenv("TESTING"):
    DATABASE_URL = "sqlite:///:memory:"

# Create an engine instance
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session
ScopedSession = scoped_session(SessionLocal)

# Base class for declarative class definitions
Base = declarative_base()

Base.query = ScopedSession.query_property()


# Dependency to use in FastAPI route to get a database session
def get_db():
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()
