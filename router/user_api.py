from datetime import datetime, timedelta, timezone
from typing import Annotated

from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from starlette import status

from data_constraints.input_schema import UsersRegisterSchema, UsersUpdateSchema
from database import db_dependency, Users
from utils import status_response_error, sql_result_to_dict


router = APIRouter(prefix="/api/user", tags=["User API"])

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

token_expires_delta = timedelta(minutes=30)
secret_key = "secret"
jwt_algorithm = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def validate_user_credential(token_to_validate: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token_to_validate, secret_key, jwt_algorithm)
        username = payload.get("sub")
        if username is None:
            status_response_error(401, "Token is Invalid")
    except ExpiredSignatureError:
        status_response_error(401, "Token has expired")
    except JWTError:
        status_response_error(401, "Token is Invalid")
    return username
user_dependency = Annotated[str, Depends(validate_user_credential)]



@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_to_register: UsersRegisterSchema, db:db_dependency):
    user_to_register = Users(
        email=user_to_register.email,
        username=user_to_register.username,
        first_name=user_to_register.first_name,
        last_name=user_to_register.last_name,
        hashed_password=crypt_context.hash(user_to_register.password),
    )
    db.add(user_to_register)
    try:
        db.flush()
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        if "UNIQUE constraint failed: Users.email" == error_msg:
            status_response_error(400, f"Email already exists: {user_to_register.email}")
        if "UNIQUE constraint failed: Users.username" == error_msg:
            status_response_error(400, f"Username already exists: {user_to_register.username}")



@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(login_form: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user_to_login = db.query(Users).filter(Users.username == login_form.username).first()
    if user_to_login is None:
        status_response_error(401, "User not found")
    if not user_to_login.is_enabled:
        status_response_error(401, "User is disabled")
    if not crypt_context.verify(login_form.password, str(user_to_login.hashed_password)):
        status_response_error(401, "Incorrect password")
    user_access_token = {"sub": user_to_login.username, "exp": datetime.now(timezone.utc) + token_expires_delta}
    return {"access_token": jwt.encode(user_access_token, secret_key, jwt_algorithm), "token_type": "bearer"}


@router.get("/info", status_code=status.HTTP_200_OK)
async def current_user_info(user: user_dependency, db:db_dependency):
    user_information = (db.query(Users.username, Users.first_name, Users.last_name, Users.email, Users.is_enabled).
                        filter(Users.username == user).first())
    return sql_result_to_dict(user_information)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: user_dependency, db:db_dependency, user_info: UsersUpdateSchema):
    user_to_update = db.query(Users).filter(Users.username == user).first()
    user_info = user_info.model_dump(exclude_unset=True)
    if "new_password" in user_info.keys() and "old_password" in user_info.keys():
        if not crypt_context.verify(user_info["old_password"], str(user_to_update.hashed_password)):
            status_response_error(401, "Incorrect old password")
        user_info["hashed_password"] = crypt_context.hash(user_info["new_password"])
    # del old_pass and new_pass if any
    user_info.pop("new_password", None)
    user_info.pop("old_password", None)
    for k, v in user_info.items():
        setattr(user_to_update, k, v)
    db.add(user_to_update)
    db.flush()