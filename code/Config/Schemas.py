from typing import List, Optional, Union
from datetime import date

from pydantic import BaseModel, EmailStr


# SCHEMAS FOR THE USER

class UserBase(BaseModel):
    email: EmailStr
    name: str
    # username: str
    contact: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        

class UserOut(UserBase):
    id : int
    class Config:
        orm_mode = True

class UserEdit(UserBase):
    password: Optional[str] = None

    class Config:
        orm_mode = True

            
# SCHEMAS FOR THE LOGIN & TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
    
    


# SCHEMAS FOR THE SMS    
class SmsBase(BaseModel):
    numero: str
    message: str
    

# SCHEMAS FOR THE SMS    

class ProduceBase(BaseModel):
    id : int
    first_player_name:str
    second_player_name:str
    result: str
    status: bool
    date: date
    accurracy: float
    users_id: int
    match_key: str
    
    
#SCHEMAS FOR PRE_MATCH_ANALISIS
class PreMatchAnalisisBase(BaseModel):
    first_player_name: str
    second_player_name: str
    date: date
    result: str
    accurracy: float
    status: bool
    users_id: int
    match_key: str
    
    # id: str
    # player1: str
    # player2: str

class PreMatchAnalisisCreate(PreMatchAnalisisBase):
    pass



