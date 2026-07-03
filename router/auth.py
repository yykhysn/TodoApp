from typing import Annotated
from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schema import UsersSchema
from database import db_dependency, Users



router = APIRouter()

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/user/register")
async def register_user(user_to_register: UsersSchema, db:db_dependency):
    print(user_to_register)
    user_to_register = Users(
        email=user_to_register.email,
        username=user_to_register.username,
        first_name=user_to_register.first_name,
        last_name=user_to_register.last_name,
        hashed_password=crypt_context.hash(user_to_register.password),
    )
    db.add(user_to_register)
    db.commit()

@router.post("/user/login")
async def login_user(login_form: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user_to_login = db.query(Users).filter(Users.username == login_form.username).first()
    if user_to_login is None:
        return "User not found"
    if not crypt_context.verify(login_form.password, str(user_to_login.hashed_password)):
        return "Incorrect password"
    return f"Welcome, {login_form.username}!"