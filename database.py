from sqlite3 import DatabaseError

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from models import Base, Words, Requests, Actions
from constants import SQLALCHEMY_SQLITE_DATABASE_URL, INITIAL_DICTIONARY_FILE

engine = create_engine(SQLALCHEMY_SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create tables from models if it does not already exist
Base.metadata.create_all(bind=engine)


def get_db():
    """
    get db as yield - open and close the connection
    :return: generator
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def row_handler(row_result):
    if not row_result:
        return 0
    return row_result[0]



