import time

from fastapi import Query, APIRouter
from typing import Optional
from starlette import status

from database import ToDoListTable, Users, db_dependency
from data_constraints.input_schema import ToDosCreateSchema, ToDosUpdateSchema
from router.user_api import user_api_dependency
from utils import sql_result_to_dict, status_response_error
from data_constraints.constants import *


router = APIRouter(prefix="/api/todos", tags=["Todos API"])


@router.get("/search", status_code=status.HTTP_200_OK)
def search_todos(db: db_dependency, user:user_api_dependency,
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
    return sql_result_to_dict(query.all())


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_todos(user: user_api_dependency, db: db_dependency, new_todo: ToDosCreateSchema):
    user_id = db.query(Users).filter(Users.username == user).first().id
    new_todo = ToDoListTable(**new_todo.model_dump(), owner_user_id=user_id)
    db.add(new_todo)
    db.flush()
    return {"detail": f"{new_todo.title}'s Todo created successfully"}


@router.put("/update", status_code=status.HTTP_200_OK)
def update_todos(db: db_dependency, user:user_api_dependency, updated_todo: ToDosUpdateSchema,
                 todo_public_uuid: str = Query(min_length=TODOS_PUBLIC_UUID_LENGTH, max_length=TODOS_PUBLIC_UUID_LENGTH)):
    record_to_update = (db.query(ToDoListTable).join(Users, Users.id == ToDoListTable.owner_user_id).
                        filter(Users.username == user, ToDoListTable.public_uuid == todo_public_uuid).first())
    if record_to_update is None:
        status_response_error(404, "Todos not found")

    old_todo_value = {
        "title": record_to_update.title,
        "description": record_to_update.description,
        "priority": record_to_update.priority,
        "is_completed": record_to_update.is_completed
    }

    todo_updated_data = updated_todo.model_dump(exclude_unset=True)
    for key, value in todo_updated_data.items():
        setattr(record_to_update, key, value)
    new_todo_value = {
        "title": record_to_update.title,
        "description": record_to_update.description,
        "priority": record_to_update.priority,
        "is_completed": record_to_update.is_completed
    }

    db.add(record_to_update)
    db.flush()

    return {
        "code": 0,
        "message": "Todo updated successfully",
        "data": {
            "before": old_todo_value,
            "after": new_todo_value
        },
        "timestamp": int(time.time())
    }


@router.get("/getAll", status_code=status.HTTP_200_OK)
def get_all_todos(db: db_dependency, user: user_api_dependency):
    todos_result = (db.query(ToDoListTable.title, ToDoListTable.description, ToDoListTable.priority,
                             ToDoListTable.is_completed, ToDoListTable.public_uuid)
                    .join(Users, Users.id == ToDoListTable.owner_user_id).filter(Users.username == user)
                    .order_by(ToDoListTable.is_completed.asc(), ToDoListTable.priority.asc()).all())
    return sql_result_to_dict(todos_result)


@router.delete("/deleteTodo", status_code=status.HTTP_200_OK)
def delete_todo(db: db_dependency, user: user_api_dependency,
                todo_public_uuid: str = Query(min_length=TODOS_PUBLIC_UUID_LENGTH, max_length=TODOS_PUBLIC_UUID_LENGTH)):
    record_to_delete = (db.query(ToDoListTable).join(Users, Users.id == ToDoListTable.owner_user_id).
                        filter(Users.username == user, ToDoListTable.public_uuid == todo_public_uuid).first())
    if record_to_delete is None:
        status_response_error(404, "Todos not found")

    db.delete(record_to_delete)
    db.flush()

    return {
        "code": 0,
        "message": "Todo deleted successfully",
        "data": {
            "title": record_to_delete.title,
            "description": record_to_delete.description,
            "priority": record_to_delete.priority,
            "is_completed": record_to_delete.is_completed
        },
        "timestamp": int(time.time())
    }