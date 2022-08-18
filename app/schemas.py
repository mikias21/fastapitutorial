from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime 
from pydantic.types import conint

class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = False

class CreatePost(PostBase):
    pass 
    
class UserCreate(BaseModel):
    email: EmailStr 
    password: str 

class UserRegResponse(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

    class config:
        orm_mode = True

class PostResponse(PostBase):
    id: int 
    created_at: datetime
    owner_id: int 
    owner: UserRegResponse

    class Config:
        orm_mode = True

class PostOut(PostBase):
    Post: PostResponse
    num_of_likes: int

    class config:
        orm_mode = True

class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None 

class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1)