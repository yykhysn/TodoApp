from typing import Annotated, Optional

from fastapi import FastAPI, Depends, Query

from sqlalchemy.orm import Session

from database import SessionLocal, ToDoListTable

from todos import ToDosCreate

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/debugDatabase")
def read_all_todolist_table(db: db_dependency):
    return db.query(ToDoListTable).all()

@app.get("/searchTodos")
def search_todos(db: db_dependency,
                 priority: Optional[int] = Query(ge=1, le=4, default=None)):
    if priority is None:
        return read_all_todolist_table(db)
    records = db.query(ToDoListTable).filter(ToDoListTable.priority == priority).all()
    if records:
        return records
    else:
        return "No such todos"

@app.post("/createTodos")
def create_todos(db: db_dependency, new_todo: ToDosCreate):
    new_todo = ToDoListTable(**new_todo.model_dump())
    db.add(new_todo)
    db.commit()