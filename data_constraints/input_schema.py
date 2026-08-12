from typing import Optional

from pydantic import BaseModel, Field

from data_constraints.constants import *


class ToDosInputSchema(BaseModel):
    title: str = Field(max_length=TODOS_TITLE_MAX_LEN)
    description: str = Field(max_length=TODOS_DESC_MAX_LEN)
    priority: int = Field(ge=TODOS_PRIORITY_MIN, le=TODOS_PRIORITY_MAX)
    is_completed: bool = Field(default=TODOS_COMPLETED_DEFAULT)


class UsersRegisterSchema(BaseModel):
    username: str = Field(max_length=USERS_USERNAME_MAX_LEN)
    password: str = Field(max_length=USERS_FIRSTNAME_MAX_LEN, min_length=USERS_PASSWORD_MIN_LEN)
    email: str = Field(max_length=USERS_EMAIL_MAX_LEN)
    first_name: str = Field(max_length=USERS_FIRSTNAME_MAX_LEN)
    last_name: str = Field(max_length=USERS_LASTNAME_MAX_LEN)


class UsersUpdateSchema(BaseModel):
    old_password: Optional[str] = Field(max_length=USERS_PASSWORD_MAX_LEN, min_length=USERS_PASSWORD_MIN_LEN, default=None)
    new_password: Optional[str] = Field(max_length=USERS_PASSWORD_MAX_LEN, min_length=USERS_PASSWORD_MIN_LEN, default=None)
    email: Optional[str] = Field(max_length=USERS_EMAIL_MAX_LEN, default=None)
    first_name: Optional[str] = Field(max_length=USERS_FIRSTNAME_MAX_LEN, default=None)
    last_name: Optional[str] = Field(max_length=USERS_LASTNAME_MAX_LEN, default=None)
    is_enabled: Optional[bool] = Field(default=None)
