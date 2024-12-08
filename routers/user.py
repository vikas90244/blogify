from fastapi import APIRouter,Depends,HTTPException,status,Response
from blog import database
from blog import schemas, database,models
from sqlalchemy.orm import Session
from repository import user
router = APIRouter(
    prefix='/user',
    tags=['users']
)

get_db = database.get_db



@router.post('/', response_model=schemas.ShowUser)
def create_user(request:schemas.User, db:Session=Depends(get_db)):
   return user.create_user(request, db)



@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id:int, db:Session=Depends(get_db)):
   return user.get_user(id,db)