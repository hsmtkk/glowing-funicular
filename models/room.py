from sqlalchemy import Column, Integer, String
from sql_app.database import Base


class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_name = Column(String, unique=True, index=True)
    capacity = Column(Integer)
