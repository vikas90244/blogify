from fastapi import APIRouter,Depends,HTTPException,status
from blog import schemas
from sqlalchemy.orm import Session
from blog import database,models
from blog.hashing import Hash
from blog.token import create_access_token
router = APIRouter(
    tags=['authentication']
)

get_db=database.get_db

@router.post('/login')
def login(request:schemas.Login, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with email doesn't exist ")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"incorrect password")
    
    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")
