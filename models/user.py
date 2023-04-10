from sqlalchemy import Column, Integer, String
from sql_app.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
