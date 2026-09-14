from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from router.user_api import validate_user_credential


router = APIRouter(prefix="/user", tags=["User Pages"])

templates = Jinja2Templates(directory="templates")

def get_web_user(request: Request):
    user_access_token = request.cookies.get("user_access_token")
    if user_access_token:
        try:
            current_login_user = validate_user_credential(user_access_token)
            return current_login_user
        except HTTPException as exception:
            if exception.status_code == 401:
                raise WebUnauthenticatedException
            else:
                raise exception
    raise WebUnauthenticatedException

user_web_dependency = Annotated[str, Depends(get_web_user)]


class WebUnauthenticatedException(Exception):
    @staticmethod
    def redirect_to_login(request: Request, exception: Exception):
        return RedirectResponse("/user/redirectToLogin.html", status_code=status.HTTP_302_FOUND)