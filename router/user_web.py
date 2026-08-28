from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/user", tags=["User Pages"])

templates = Jinja2Templates(directory="templates/user")


@router.get("/login.html")
def user_login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.get("/register.html")
def user_register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")