from app.db.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, autoincrement=True)
    propertyId=Column(Integer)
    name = Column(String)



class ImageBase(BaseModel):
    name: str 
    propertyId:int
    id: int
