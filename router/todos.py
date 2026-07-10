from fastapi import Query, APIRouter
from typing import Optional
from starlette import status

from database import ToDoListTable, Users, db_dependency
from config.input_schema import ToDosInputSchema
from router.user import user_dependency
from utils import sql_rows_to_dict, status_response_error
from config.constants import *



router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("/debugDatabase")
def read_all_todolist_table(db: db_dependency):
    return db.query(ToDoListTable).all()

@router.get("/search", status_code=status.HTTP_200_OK)
def search_todos(db: db_dependency, user:user_dependency,
                 priority: Optional[int] = Query(ge=TODOS_PRIORITY_MIN, le=TODOS_PRIORITY_MAX, default=None),
                 title: Optional[str] = Query(max_length=TODOS_TITLE_MAX_LEN, default=None),
                 description: Optional[str] = Query(max_length=TODOS_DESC_MAX_LEN, default=None),
                 is_completed: Optional[bool] = Query(default=None)):
    query = (db.query(ToDoListTable.title, ToDoListTable.description, ToDoListTable.priority,
                      ToDoListTable.is_completed, ToDoListTable.public_uuid).
             join(Users, Users.id == ToDoListTable.owner_user_id).filter(Users.username == user))
    if priority is not None:
        query = query.filter(ToDoListTable.priority == priority)
    if title is not None:
        query = query.filter(ToDoListTable.title.like(f"%{title}%"))
    if description is not None:
        query = query.filter(ToDoListTable.description.like(f"%{description}%"))
    if is_completed is not None:
        query = query.filter(ToDoListTable.is_completed == is_completed)
    return sql_rows_to_dict(query.all())

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_todos(user: user_dependency, db: db_dependency, new_todo: ToDosInputSchema):
    user_id = db.query(Users).filter(Users.username == user).first().id
    new_todo = ToDoListTable(**new_todo.model_dump(), owner_user_id=user_id)
    db.add(new_todo)
    db.commit()
    return f"Success! {new_todo.title}'s todo has been created!"

@router.put("/update")
def update_todos(db: db_dependency, user:user_dependency,
                 public_uuid: str = Query(min_length=32, max_length=32),
                 priority: Optional[int] = Query(ge=TODOS_PRIORITY_MIN, le=TODOS_PRIORITY_MAX, default=None),
                 title: Optional[str] = Query(max_length=TODOS_TITLE_MAX_LEN, default=None),
                 description: Optional[str] = Query(max_length=TODOS_DESC_MAX_LEN, default=None),
                 is_completed: Optional[bool] = Query(default=None)):
    record_to_update = (db.query(ToDoListTable).join(Users, Users.id == ToDoListTable.owner_user_id).
                        filter(Users.username == user, ToDoListTable.public_uuid == public_uuid).first())
    if record_to_update is None:
        status_response_error(404, "Todos not found")
    if priority is not None:
        record_to_update.priority = priority
    if title is not None:
        record_to_update.title = title
    if description is not None:
        record_to_update.description = description
    if is_completed is not None:
        record_to_update.is_completed = is_completed
    db.commit()

@router.get("/getAll", status_code=status.HTTP_200_OK)
def get_all_todos(db: db_dependency, user: user_dependency):
    todos_result = (db.query(ToDoListTable.title, ToDoListTable.description, ToDoListTable.priority,
                            ToDoListTable.is_completed, ToDoListTable.public_uuid).
                    join(Users, Users.id == ToDoListTable.owner_user_id).filter(Users.username == user).all())
    return sql_rows_to_dict(todos_result)