from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/user", tags=["User Pages"])

templates = Jinja2Templates(directory="templates")