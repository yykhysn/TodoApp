import string

from pydantic import BaseModel, Field



class ToDosSchema(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=64)
    priority: int = Field(ge=1, le=4)
    is_completed: bool = Field(default=False)
    owner_user_id: int = Field(max_length=8)


class UsersSchema(BaseModel):
    username: str = Field(max_length=32)
    password: str = Field(max_length=32, min_length=16)
    email: str = Field(max_length=64)
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)