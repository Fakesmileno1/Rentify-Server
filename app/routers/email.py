from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter ,HTTPException, status
from fastapi.responses import RedirectResponse 
from app.db.database import get_db
from app.models.email import BlogsBase,Blogs
import smtplib

app = APIRouter()

@app.post('about')
def index(blogs:BlogsBase,db: Session = Depends(get_db)):
    receiver = f'{blogs.mail}'
    sender = 'balaji200214@gmail.com'
    message = f'{blogs.name},{blogs.phonenumber}'
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender, "nudxvfyepzzjygwb")
    server.sendmail(sender,receiver,message)


