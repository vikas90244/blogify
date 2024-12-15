from sqlalchemy.orm import Session
from blog import models,schemas
from fastapi import HTTPException,status

def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request:schemas.Blog, db:Session, id:int ):
    new_blog = models.Blog(title=request.title, body = request.body, user_id=id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

def destroy(id, db:Session, user_id:int):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")
    
    if blog.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this blog"
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'



def update(id, request:schemas.Blog, db:Session, user_id:int):

    blog=db.query(models.Blog).filter(models.Blog.id==id )
    if not blog.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")
    
    if blog.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this blog"
        )
    blog.update(request.dict())
    db.commit()
    return 'updated'


def show(id, db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"blog with id {id} not found")

    #    response.status_code =status.HTTP_404_NOT_FOUND
    #    return {'detail':status.HTTP_404_NOT_FOUND}                   
    return blog

