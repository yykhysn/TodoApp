from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from config.input_schema import UsersInputSchema
from database import db_dependency, Users
from utils import status_response_error



router = APIRouter(prefix="/user", tags=["User"])

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

token_expires_delta = timedelta(minutes=30)
secret_key = "secret"
jwt_algorithm = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


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



@router.post("/register")
async def register_user(user_to_register: UsersInputSchema, db:db_dependency):
    user_to_register = Users(
        email=user_to_register.email,
        username=user_to_register.username,
        first_name=user_to_register.first_name,
        last_name=user_to_register.last_name,
        hashed_password=crypt_context.hash(user_to_register.password),
    )
    db.add(user_to_register)
    db.commit()

@router.post("/login")
async def login_user(login_form: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user_to_login = db.query(Users).filter(Users.username == login_form.username).first()
    if user_to_login is None:
        status_response_error(401, "User not found")
    if not crypt_context.verify(login_form.password, str(user_to_login.hashed_password)):
        status_response_error(401, "Incorrect password")
    user_access_token = {"sub": user_to_login.username, "exp": datetime.now(timezone.utc) + token_expires_delta}
    return {"access_token": jwt.encode(user_access_token, secret_key, jwt_algorithm), "token_type": "bearer"}