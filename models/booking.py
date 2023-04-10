from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sql_app.database import Base
from models.user import User
from models.room import Room


class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey(User.user_id, ondelete="SET NULL"), nullable=True
    )
    room_id = Column(
        Integer, ForeignKey(Room.room_id, ondelete="SET NULL"), nullable=True
    )
    booked_num = Column(Integer)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
