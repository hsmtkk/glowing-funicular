from pydantic import BaseModel, Field

import config


class RoomCreate(BaseModel):
    room_name: str = Field(max_length=config.ROOM_NAME_MAX)
    capacity: int


class Room(RoomCreate):
    room_id: int

    class Config:
        orm_mode = True
