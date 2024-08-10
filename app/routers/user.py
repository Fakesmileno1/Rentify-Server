from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter ,HTTPException, status
from fastapi.responses import RedirectResponse 
from app.db.database import get_db
from app.models.user import UserBase, User,LoginBase
from passlib.context import CryptContext

app = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@app.post("/")
def index(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(firstname=user.firstname, lastname=user.lastname, email=user.email, phonenumber=user.phonenumber, password=pwd_context.hash(user.password), type=user.type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    print(user.email, password, user.password)
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user

@app.post("/login")
def login(user: LoginBase, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return user




@app.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
