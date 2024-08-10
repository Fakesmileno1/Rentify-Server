from app.db.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel


class Blogs(Base):
    __tablename__ = "email"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    mail = Column(String)
    phonenumber=Column(String)
    message = Column(String)



class BlogsBase(BaseModel):
    name:str
    mail:str
    phonenumber:str
    message:str