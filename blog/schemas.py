from pydantic import BaseModel, EmailStr
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str
    title_color: str = "#e2efff"


class Blog(BlogBase):
    class Config():
        from_attributes = True



class User(BaseModel):
    name: str
    email: str
    password: str

class CurrentUser(BaseModel):
    id: int
    name: str
    email: str


class ShowUser(BaseModel):
    id
    name: str
    email: str
    blogs: List[Blog] = []
    class Config():
        from_attributes = True



class ShowBlog(Blog):
    id: int
    creator: ShowUser
    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class EmailSchema(BaseModel):
    email: EmailStr

class RegisterWithOTP(BaseModel):
    name: str
    email: EmailStr
    password: str
    otp: str