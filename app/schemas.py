import json
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.networks import EmailStr
from pydantic.types import conint

from sqlalchemy import orm
from sqlalchemy.sql.sqltypes import BIGINT, String

from app.models import User


# Extending Base model of pydantic (Validating The data we get from request)
class PostBase(BaseModel):  # 4
    related_text: str
    published: bool = True
    images: list  # optional Feild
    # rating: Optional[int] = None  # fully optional feild


class CommentBase(BaseModel):
    post_id: int
    # user_id: int
    comment: str


class UploadImageRes(BaseModel):
    image_url: str


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    about: str
    profile_photo: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserRelationResponse(BaseModel):
    id: int
    username: str
    full_name: str
    profile_photo: str

    class Config:
        orm_mode = True


class CommentResponse(CommentBase):
    id: int
    user_id: int
    user: UserRelationResponse

    class Config:
        orm_mode = True


class Profile(BaseModel):
    User: UserResponse
    followers_count: int
    following_count: int
    is_followed_by_viewer: bool

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserRelationResponse
    comments: List[CommentResponse]

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
    is_liked_by_viewer: Optional[bool]
    pass

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    full_name: Optional[str]
    email: EmailStr
    password: str
    about: Optional[str]
    profile_photo: Optional[str]


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


class ChatResponse(BaseModel):
    id: int
    users: List[UserRelationResponse]

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    content: str
    chat_id: int


class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    sender: UserRelationResponse

    class Config:
        orm_mode = True


class PaginatedMessageResponse(BaseModel):
    messages: List[MessageResponse]
    total_pages: int

    class Config:
        orm_mode = True


class UserListResponse(BaseModel):
    User: UserRelationResponse
    is_followed_by_viewer: bool

    class Config:
        orm_mode = True
