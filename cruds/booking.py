from sqlalchemy.orm import Session
import config
import models.booking
import schemas.booking


def list(db: Session, skip: int = 0, limit: int = config.DEFAULT_LIMIT):
    return db.query(models.booking.Booking).offset(skip).limit(limit).all()


def get(db: Session, booking_id: int):
    return (
        db.query(models.booking.Booking)
        .filter(models.booking.Booking.booking_id == booking_id)
        .first()
    )


def create(db: Session, booking: schemas.booking.Booking):
    booking = models.booking.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        booked_num=booking.booked_num,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
