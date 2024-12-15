from fastapi import APIRouter,Depends,status,Response
from blog import database
from blog import schemas, database,Oauth2
from sqlalchemy.orm import Session
from repository import blog

router = APIRouter(
     prefix="/blog",
     tags=['blogs']
)

get_db = database.get_db

@router.get('/', response_model=list[schemas.ShowBlog])
def all(db: Session=Depends(database.get_db)):
   return blog.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db:Session=Depends(get_db), get_current_user:schemas.User=Depends(Oauth2.get_current_user)):
    return blog.create(request, db, get_current_user.id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,  db:Session=Depends(get_db), get_current_user:schemas.ShowUser = Depends(Oauth2.get_current_user)):
    return blog.destroy(id,db, get_current_user.id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db:Session=Depends(get_db), get_current_user:schemas.User=Depends(Oauth2.get_current_user)):
    return blog.update(id, request, db,get_current_user.id)



@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, response:Response, db:Session =Depends(get_db)):
   return blog.show(id, db)
