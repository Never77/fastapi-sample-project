from sqlalchemy.orm import Session
from fastapi_test import models, schemas
import logging
from uuid import uuid4


def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserIn):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, id : uuid4):
    return db.query(models.User).filter(models.User.id == id).first()

def delete_user_by_id(id: uuid4, db: Session):
    db_user = get_user_by_id(id=id, db=db)
    db.delete(db_user)
    logging.debug(f"Deleted user with ID {id}")
    db.commit()
    return id
    # return db.delete(db_user).returning(models.User.id, models.User.name)  # If we wanna change strategy