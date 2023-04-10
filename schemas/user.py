from pydantic import BaseModel, Field

import config


class UserCreate(BaseModel):
    username: str = Field(max_length=config.USERNAME_MAX)


class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True
