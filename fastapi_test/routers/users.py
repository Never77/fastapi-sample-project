from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_test.database import get_database
from fastapi_test.crud import user as crud
from typing import List
from fastapi_test.schemas import users as schemas
from pydantic import UUID4

router = APIRouter(prefix='/users', tags=["users"])

@router.get('/', response_model=List[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    return crud.list_users(skip=skip, limit=limit, db=db)

@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserIn, db:Session = Depends(get_database)):
    return crud.create_user(db=db, user=user)

@router.get('/{id}', response_model=schemas.User)
def get_user_by_id(id: UUID4, db: Session = Depends(get_database)):
    return crud.get_user_by_id(db=db, id=id)

@router.delete('/{id}', status_code=204)
def delete_user_by_id(id: UUID4, db: Session = Depends(get_database)):
    return crud.delete_user_by_id(id=id, db=db)

# TODO: Need a route to update the user by id