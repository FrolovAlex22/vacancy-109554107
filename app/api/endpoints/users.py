from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.endpoints.user_utils import (
    get_current_user_for_refresh,
    validate_auth_user
)
from app.api.schemas.users import (
    TokenInfo,
    UserCreate,
    UserLogin,
    UserResponse
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_pass
)
from app.db.database import get_db_session
from app.db.models import User


http_bearer = HTTPBearer(auto_error=False)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", status_code=status.HTTP_200_OK,)
async def index():
    return {"status": "fastapi task_manager service is running."}


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db_session)
):
    """Создание аккаунта юзера."""

    hashed_pass = hash_pass(user_in.password_hash)

    user = User(
        username=user_in.username,
        password_hash=hashed_pass,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.post("/register/", response_model=TokenInfo)
async def login(
    user: UserLogin = Depends(validate_auth_user),
):
    """Авторизация юзера."""

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "password_hash": user.password_hash,
        }
    )
    refresh_token = create_refresh_token(data={"user_id": user.id})

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    user: UserLogin = Depends(get_current_user_for_refresh)
):
    """Обновление acces токена."""

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "password_hash": user.password_hash,
        }
    )
    return TokenInfo(
        access_token=access_token,
    )
