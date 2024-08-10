from app.db.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from typing import List, Optional
from app.models.image import ImageBase

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer)
    name = Column(String)
    street = Column(String)
    district = Column(String)
    state = Column(String)
    housetype = Column(String)
    floor = Column(Integer)
    numberofbedroom = Column(Integer)
    numberofbathroom = Column(Integer)
    hospital = Column(Integer)
    school = Column(Integer)
    college = Column(Integer)
    price = Column(Integer)
   
class PropertyBase(BaseModel):
    id: int
    userid: int
    name: str
    street: str
    district : str
    state: str
    housetype: str
    floor: int
    numberofbedroom: int
    numberofbathroom: int
    hospital: int
    school: int
    college: int
    price: int
    image: List[ImageBase] = []
  
 
class PropertyUpdate(BaseModel):
    name: Optional[str]
    street: Optional[str]
    district: Optional[str]
    state: Optional[str]
    housetype: Optional[str]
    floor: Optional[int]
    numberofbedroom: Optional[int]  
    numberofbathroom: Optional[int]
    hospital: Optional[int]
    school: Optional[int]
    college: Optional[int]
    price: Optional[int]
    imagename:Optional[str]


class PropertyResponse(PropertyBase):
    id: int

    class Config:
        orm_mode: True