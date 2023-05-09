import json
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.networks import EmailStr
from pydantic.types import conint

from sqlalchemy import orm
from sqlalchemy.sql.sqltypes import BIGINT, String

from app.models import User

# Extending Base model of pydantic (Validating The data we get from request)
class PostBase(BaseModel):  # 4
    title: str
    content: str
    published: bool = True
    image: Optional[str]  # optional Feild
    # rating: Optional[int] = None  # fully optional feild


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class Postwithout(BaseModel):
    id: int
    content: str
    created_at: str
    title: str
    created_at: datetime
    published: bool = True
    owner_id: int


class Postwith(BaseModel):
    post: PostResponse
    votes: int
    pass

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ResponseToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
