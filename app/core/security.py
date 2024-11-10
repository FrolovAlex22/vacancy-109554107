from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from jwt import PyJWTError

from app.core.config import settings
from app.api.schemas.users import DataToken, UserBaseSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = settings.AUTH.KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    token_data.update({TOKEN_TYPE_FIELD: token_type})
    to_encode = token_data.copy()
    if expire_timedelta:
        expire = datetime.now() + timedelta(minutes=expire_timedelta)
    else:
        expire = datetime.now() + timedelta(minutes=expire_minutes)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def hash_pass(password: str):
    return pwd_context.hash(password)


def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)


def create_access_token(data: dict):
    return create_jwt(ACCESS_TOKEN_TYPE, data)
    # to_encode = data.copy()
    # expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    # return encoded_jwt

def create_refresh_token(data: dict) -> str:
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=data,
        expire_timedelta=REFRESH_TOKEN_EXPIRE_MINUTES
    )


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = DataToken(id=id)
    except PyJWTError as e:
        print(e)
        raise credentials_exception
    return token_data


# @router.post("/login/", response_model=Token)
# async def login(
#     userdetails: OAuth2PasswordRequestForm = Depends(),
#     session: AsyncSession = Depends(get_db_session),
# ):
#     """Авторизация юзера."""

#     stmt = select(User).filter(userdetails.username == User.username)
#     result = await session.execute(stmt)
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist"
#         )
#     if not verify_password(userdetails.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
#         )
#     access_token = create_access_token(data={"user_id": user.id})
#     return {"access_token": access_token, "token_type": "Bearer"}