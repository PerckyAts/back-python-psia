from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from Config.Model import User
from Config.Schemas import User, UserCreate, UserEdit
from Crud.User_crud import get_user, get_user_by_email, get_users, edit_user
from Config.Database import SessionLocal, engine, get_db


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.get("/get_all_users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/edit_users/{user_id}", response_model=User)
def edit_profil_user(user_id: int, user: UserEdit, db: Session = Depends(get_db)):
    user_edit= edit_user(db , user_id, user) 
    return user_edit
#push


