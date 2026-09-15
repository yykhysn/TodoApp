from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates

from database import Users, db_dependency
from router.todos_api import get_all_todos
from router.user_web import user_web_dependency


router = APIRouter(prefix="/todos", tags=["Todos Pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/todo.html")
def todo_page(request: Request, user: user_web_dependency, db: db_dependency):
    current_login_user_lastname = db.query(Users).filter(Users.username == user).first().last_name
    current_login_user_todos = get_all_todos(db, user)
    return templates.TemplateResponse(request, "/todos/todo.html",
                                      {"current_login_user_lastname": current_login_user_lastname,
                                       "current_login_user_todos": current_login_user_todos})