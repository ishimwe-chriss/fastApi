from datetime import datetime

from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    model_config = {
        "from_attributes": True
    }


class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
