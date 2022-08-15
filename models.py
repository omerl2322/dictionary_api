from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base

# sqlalchemy model tables
Base = declarative_base()


class Words(Base):
    __tablename__ = "words"

    word = Column(String, primary_key=True, index=True)

    def __repr__(self):
        return self.word


class Requests(Base):
    __tablename__ = "api_requests"

    request_number = Column(Integer, primary_key=True, autoincrement=True)
    request_handle_time = Column(Numeric(10, 3))  # millisecond


class Actions(Base):
    __tablename__ = "api_actions"

    action = Column(String)
    request_id = Column(String, primary_key=True, index=True)
    status = Column(String)
