import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, FetchedValue
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv


load_dotenv(dotenv_path="./database_configuration/data_source_config")
DATABASE_URL = os.getenv("DATABASE_URL")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]


class ToDoListTable(Base):
    __tablename__ = "ToDoList"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    is_completed = Column(Boolean, server_default=FetchedValue(), nullable=False)
    owner_user_id = Column(Integer, ForeignKey("Users.id"), index=True, nullable=False)
    public_uuid = Column(String, unique=True, server_default=FetchedValue(), nullable=False)


class Users(Base):
    __tablename__ = "Users"
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    id = Column(Integer, primary_key=True)