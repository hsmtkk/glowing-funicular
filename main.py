from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

import cruds.booking
import cruds.room
import cruds.user
import schemas.user
import schemas.booking
import schemas.room

from sql_app.database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=List[schemas.user.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cruds.user.list(db, skip, limit)


@app.get("/rooms", response_model=List[schemas.room.Room])
async def get_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cruds.room.list(db, skip, limit)


@app.get("/bookings", response_model=List[schemas.booking.Booking])
async def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cruds.booking.list(db, skip, limit)


@app.post("/users", response_model=schemas.user.User)
async def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    return cruds.user.create(db, user)


@app.post("/rooms", response_model=schemas.room.Room)
async def create_room(room: schemas.room.RoomCreate, db: Session = Depends(get_db)):
    return cruds.room.create(db, room)


@app.post("/bookings", response_model=schemas.booking.Booking)
async def create_booking(
    booking: schemas.booking.BookingCreate, db: Session = Depends(get_db)
):
    return cruds.booking.create(db, booking)
