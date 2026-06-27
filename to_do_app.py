from typing import Annotated

from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from database import SessionLocal, ToDoList

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/debugDatabase")
def debug_database(db: db_dependency):
    return db.query(ToDoList).all()