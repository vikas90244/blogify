from pydantic import BaseModel, EmailStr
from typing import List

class BlogBase(BaseModel):
    title:str
    body:str
    title_color:str


class Blog(BlogBase):
    class Config():
        from_attributes = True



class User(BaseModel):
    id:int
    name:str
    email:str
    password:str



class ShowUser(BaseModel):
    name:str
    email:str
    blogs:List[Blog]=[]
    class Config():
        from_attributes = True



class ShowBlog(Blog):
    id:int
    creator: ShowUser
    class Config():
        from_attributes = True


class Login(BaseModel):
    username:str
    password:str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class EmailSchema(BaseModel):
    email: EmailStr

class RegisterWithOTP(BaseModel):
    name:str
    email: EmailStr
    password:str
    otp: str