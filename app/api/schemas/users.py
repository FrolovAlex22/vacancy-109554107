from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBaseSchema(BaseModel):
    username: str


class UserCreate(UserBaseSchema):
    username: str
    password_hash: str


class UserResponse(UserBaseSchema):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    id: int | None = None
