from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.schemas.users import Token, UserBaseSchema, UserCreate, UserResponse
from app.core.security import create_access_token, hash_pass, verify_password
from app.db.database import get_db_session
from app.db.models import User


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


@router.post("/register/", response_model=Token)
async def login(
    userdetails: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
):
    """Авторизация юзера."""

    stmt = select(User).filter(userdetails.username == User.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist"
        )
    if not verify_password(userdetails.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}