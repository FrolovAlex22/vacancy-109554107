from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBaseSchema(BaseModel):
    username: str


class UserCreate(UserBaseSchema):
    username: str
    password_hash: str


class UserResponse(UserBaseSchema):
    id: int


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class DataToken(BaseModel):
    id: int | None = None
