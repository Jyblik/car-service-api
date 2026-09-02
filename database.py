import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# Engine -> interaction object
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session -> work with Base: .add() .delete()
SessionLokal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Model -> collums & rows
class Base(DeclarativeBase):
    pass


# Dependency injection -> when session is needed = pass it

def get_db():
    # create Session
    db = SessionLokal()

    # yield -> pass db to api & work
    try:
        yield db
    # finally -> close it
    finally:
        db.close()