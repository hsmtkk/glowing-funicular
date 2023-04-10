from sqlalchemy.orm import Session
import config
import models.user
import schemas.user


def list(db: Session, skip: int = 0, limit: int = config.DEFAULT_LIMIT):
    return db.query(models.user.User).offset(skip).limit(limit).all()


def get(db: Session, user_id: int):
    return (
        db.query(models.user.User).filter(models.user.User.user_id == user_id).first()
    )


def create(db: Session, user: schemas.user.User):
    user = models.user.User(username=user.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
