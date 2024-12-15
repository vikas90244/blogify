from fastapi import APIRouter,Depends,HTTPException,status
from blog import schemas
from sqlalchemy.orm import Session
from blog import database,models
from blog.hashing import Hash
from blog.JWTtoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
import random
import smtplib
from datetime import datetime, timedelta,timezone

router = APIRouter(
    tags=['authentication']
)

get_db=database.get_db


otp_store = {}


@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with email doesn't exist ")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"incorrect password")
    
    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")



@router.post('/register/send-otp')
def send_otp_for_registration(request:schemas.EmailSchema, db:Session =Depends(get_db)):

    if db.query(models.User).filter(models.User.email==request.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    otp = str(random.randint(100000, 999999))
    expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp_store[request.email] = {"otp": otp, "expiry": expiry}

    try:
        sender_email = "vksr90244@gmail.com"
        sender_password = "erixmsiwkybksxrb"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email, request.email,
                f"Subject: Email Verification Code\n\nYour OTP is {otp}. It expires in 5 minutes."
            )
    except Exception as e:
        
        raise HTTPException(status_code=500, detail="Failed to send email.")

    return {"message": "OTP sent successfully"}



@router.post('/register/verify-otp')
def verify_otp_and_register(request: schemas.RegisterWithOTP, db: Session = Depends(get_db)):
    stored_otp = otp_store.get(request.email)
    print(stored_otp)
    if not stored_otp:
        raise HTTPException(status_code=404, detail="OTP not found")

    if datetime.now(timezone.utc) > stored_otp["expiry"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    if stored_otp["otp"] != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP is valid - proceed to create user
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Clear OTP after successful registration
    del otp_store[request.email]

    return {"message": "User registered successfully"}
