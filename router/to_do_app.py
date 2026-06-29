from fastapi import Depends, Query, APIRouter

from typing import Annotated, Optional

from sqlalchemy.orm import Session

from database import SessionLocal, ToDoListTable
from todos import ToDosSchema



router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/debugDatabase")
def read_all_todolist_table(db: db_dependency):
    return db.query(ToDoListTable).all()

@router.get("/searchTodos")
def search_todos(db: db_dependency,
                 priority: Optional[int] = Query(ge=1, le=4, default=None)):
    if priority is None:
        return read_all_todolist_table(db)
    records = db.query(ToDoListTable).filter(ToDoListTable.priority == priority).all()
    if records:
        return records
    else:
        return "No such todos"

@router.post("/createTodos")
def create_todos(db: db_dependency, new_todo: ToDosSchema):
    new_todo = ToDoListTable(**new_todo.model_dump())
    db.add(new_todo)
    db.commit()

@router.put("/updateTodos")
def update_todos(db: db_dependency, todo_id: int, update_todo: ToDosSchema):
    record_to_update = db.query(ToDoListTable).get(todo_id)
    if record_to_update is not None:
        record_to_update.priority = update_todo.priority
        record_to_update.title = update_todo.title
        record_to_update.description = update_todo.description
        record_to_update.is_completed = update_todo.is_completed
        db.add(record_to_update)
        db.commit()