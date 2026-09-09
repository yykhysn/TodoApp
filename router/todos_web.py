from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from database import Users, db_dependency
from router.user_api import validate_user_credential


router = APIRouter(prefix="/todos", tags=["Todos Pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/todo.html")
def todo_page(request: Request, db: db_dependency):
    user_access_token = request.cookies.get("user_access_token")
    if user_access_token is not None:
        current_login_user = validate_user_credential(user_access_token)
        if current_login_user is not None:
            current_login_user_lastname = db.query(Users).filter(Users.username == current_login_user).first().last_name
            return templates.TemplateResponse(request, "/todos/todo.html", {"current_login_user_lastname": current_login_user_lastname})
    return RedirectResponse("/user/redirectToLogin.html", status_code=status.HTTP_302_FOUND)