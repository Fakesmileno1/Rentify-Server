from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter,HTTPException,status,File,UploadFile,Form
from app.db.database import get_db
from sqlalchemy import select, join, desc
from app.models.property import Property,PropertyUpdate, PropertyBase, List
from app.models.image import Image, ImageBase
from secrets import token_hex
import os

app = APIRouter()

image = "./image/"

@app.post("/")
async def index(
    userid: int = Form(...),
    name: str = Form(...),
    street: str = Form(...),
    district: str = Form(...),
    state: str = Form(...),
    housetype: str = Form(...),
    floor: int = Form(...),
    numberofbedroom: int = Form(...),
    numberofbathroom: int = Form(...),
    hospital: int = Form(...),
    school: int = Form(...),
    college: int = Form(...),
    price: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    os.makedirs(image, exist_ok=True)
    
    file_ext = file.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = os.path.join(image, f"{file_name}.{file_ext}")
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    db_user = Property(
        userid=userid,
        name=name,
        street=street,
        district=district,
        state=state,
        housetype=housetype,
        floor=floor,
        numberofbedroom=numberofbedroom,
        numberofbathroom=numberofbathroom,
        hospital=hospital,
        school=school,
        college=college,
        price=price,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_img = Image(name=file_path, propertyId=db_user.id)
    db.add(db_img) 
    db.commit()  
    db.refresh(db_img)
    return db_user

@app.get("/post/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(Property).filter(Property.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")  
    db.commit()
    db.refresh(post)
    return post

@app.get("/", response_model=List[PropertyBase])
def get_property(page: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    print(limit, page)

    stmt = select(Property).order_by(desc(Property.id)).offset(page).limit(limit)
    properties = db.execute(stmt).scalars().all()

    properties_responses = []
    for property in properties:
        stmt = select(Image).where(Image.propertyId == property.id)
        posts = db.execute(stmt).scalars().all()
        property_response = PropertyBase(
            id=property.id,
            name=property.name,
            userid=property.userid,
            street=property.street,
            district=property.district,
            state=property.state,
            housetype=property.housetype,
            floor=property.floor,
            numberofbedroom=property.numberofbedroom,
            numberofbathroom=property.numberofbathroom,
            hospital=property.hospital,
            school=property.school,
            college=property.college,
            price=property.price,
            image=[]
        )
        for post in posts:
            property_response.image.append(post)
        properties_responses.append(property_response)
    return properties_responses



@app.get("/user/{id}", response_model=List[PropertyBase])
def get_user_property(id: int, page: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    print(limit, page)

    stmt = select(Property).order_by(desc(Property.id)).where(Property.userid == id).offset(page).limit(limit)
    properties = db.execute(stmt).scalars().all()

    properties_responses = []
    for property in properties:
        stmt = select(Image).where(Image.propertyId == property.id)
        posts = db.execute(stmt).scalars().all()
        property_response = PropertyBase(
            id=property.id,
            name=property.name,
            userid=property.userid,
            street=property.street,
            district=property.district,
            state=property.state,
            housetype=property.housetype,
            floor=property.floor,
            numberofbedroom=property.numberofbedroom,
            numberofbathroom=property.numberofbathroom,
            hospital=property.hospital,
            school=property.school,
            college=property.college,
            price=property.price,
            image=[]
        )
        for post in posts:
            property_response.image.append(post)
        properties_responses.append(property_response)
    return properties_responses


@app.put("/{id}")
def update_property(id: int, property_update: PropertyUpdate, db: Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == id).first()
    if not db_property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    
    for key, value in property_update.dict(exclude_unset=True).items():
        setattr(db_property, key, value)
    
    db.commit()
    db.refresh(db_property)
    return db_property

@app.delete("/{id}")
def delete_property(id: int, db: Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == id).first()
    if not db_property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    
    db.delete(db_property)
    db.commit()
    return db_property