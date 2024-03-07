from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from datetime import timedelta
from Config import Security
from Config.Database import get_db
from Config.Schemas import UserCreate
from Dependencies.Dependencies import authenticate_user, sign_up_new_user


auth_router = r = APIRouter()


@r.post("/signin")
async def login(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    access_token = Security.create_access_token(
        data={
              "id":user.id,
              "email": user.email,
              "username":user.name,
              "contact":user.contact,
              },
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}




@r.post("/signup")
async def signup(db=Depends(get_db), email: str = Form(), contact: str = Form(), form_data: OAuth2PasswordRequestForm = Depends()):
    user = sign_up_new_user(db, username=form_data.username, password=form_data.password, email=email,contact=contact)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user} already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    access_token = Security.create_access_token(
        data={"sub": user.email, "password": user.password, "contact":contact},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
