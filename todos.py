from pydantic import BaseModel, Field



class ToDosSchema(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=64)
    priority: int = Field(ge=1, le=4)
    is_completed: bool = Field(default=False)