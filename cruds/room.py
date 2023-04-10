from sqlalchemy.orm import Session
import config
import models.room
import schemas.room


def list(db: Session, skip: int = 0, limit: int = config.DEFAULT_LIMIT):
    return db.query(models.room.Room).offset(skip).limit(limit).all()


def get(db: Session, room_id: int):
    return (
        db.query(models.room.Room).filter(models.room.Room.room_id == room_id).first()
    )


def create(db: Session, room: schemas.room.Room):
    room = models.room.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
