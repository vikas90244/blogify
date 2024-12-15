from fastapi import Depends,status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from blog.database import get_db
from blog import JWTtoken 
from blog import models, schemas
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depends(get_db)):
        
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},)
    
    token_data= JWTtoken.verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if not user:
        raise credentials_exception

    return user