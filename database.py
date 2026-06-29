from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



DATABASE_URL = "sqlite:///./DATA/to_do_app.sqlite3"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ToDoListTable(Base):
    __tablename__ = "ToDoList"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    owner_user_id = Column(Integer, ForeignKey("User.id"))


class Users(Base):
    __tablename__ = "Users"
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_enabled = Column(Boolean)
    id = Column(Integer, primary_key=True)