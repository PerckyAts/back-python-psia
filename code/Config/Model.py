from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date , Float
from sqlalchemy.orm import relationship
from .Database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    contact = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    


class PreMatchAnalisis(Base):
    __tablename__ = "pre_match_analisis"
    
    id=Column(Integer, primary_key=True)
    first_player_name=Column(String)
    second_player_name=Column(String)
    date=Column(Date, index=True)
    result=Column(String , index=True)
    accurracy=Column(Float, index=True)
    status=Column(Boolean, default=False)
    users_id = Column(Integer, ForeignKey("users.id")) 
    match_key=Column(String, index=True)
    # Relationships
    user = relationship("User")