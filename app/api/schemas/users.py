from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserCreate(UserBaseSchema):
    password_hash: str


class UserLogin(UserBaseSchema):
    id: int
    password_hash: str


class UserResponse(UserBaseSchema):
    id: int


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class DataToken(BaseModel):
    id: int | None = None
