from fastapi import Query, APIRouter
from typing import Optional
from starlette import status

from database import ToDoListTable, Users, db_dependency
from schema import ToDosSchema
from router.auth import user_dependency



router = APIRouter()


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

@router.post("/createTodos", status_code=status.HTTP_201_CREATED)
def create_todos(user: user_dependency, db: db_dependency, new_todo: ToDosSchema):
    user_id = db.query(Users).filter(Users.username == user).first().id
    new_todo = ToDoListTable(**new_todo.model_dump(), owner_user_id=user_id)
    db.add(new_todo)
    db.commit()
    return f"Success! {new_todo.title}'s todo has been created!"

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