from fastapi import APIRouter

from schema import UsersSchema
from database import db_dependency, Users

from passlib.context import CryptContext



router = APIRouter()

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/login")
async def login():
    return {"user": "Login on"}

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