import sys
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
from Config.Model import User
from Config.Schemas import UserBase, UserCreate, UserEdit, UserOut
from Config.Security import get_password_hash



def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_name(db: Session, username: str) -> UserBase:
    return db.query(User).filter(User.name == username).first()

def get_user_by_email(db: Session, username: str) -> UserBase:
    return db.query(User).filter(User.name == username).first()

def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[UserOut]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        contact=user.contact
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: UserEdit
) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user