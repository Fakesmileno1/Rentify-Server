from app.db.database import Base
from sqlalchemy import Column, Integer, String , Boolean
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    phonenumber = Column(Integer, unique=True)
    password = Column(String)
    type = Column(Boolean)



class LoginBase(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    phonenumber: int
    password: str
    type: bool