from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    TOKEN_TYPE_FIELD,
    decode_jwt,
    verify_access_token,
    verify_password
)
from app.db.database import get_db_session
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/register/")


CREDENTAILS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session)
):
    """Получение текущего юзера."""

    token = verify_access_token(
        token=token, credentials_exception=CREDENTAILS_EXCEPTION
    )
    stmt = select(User).where(token.id == User.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_user_for_refresh(
    token: str = Depends(oauth2_scheme),
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db_session)
):
    """Получение текущего юзера и рефреш токена."""
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type, expected 'refresh'",
        )
    print(payload)
    token = verify_access_token(
        token=token, credentials_exception=CREDENTAILS_EXCEPTION
    )
    stmt = select(User).where(token.id == User.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_db_session),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    stmt = select(User).where(username == User.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise unauthed_exc

    if not verify_password(
        non_hashed_pass=password,
        hashed_pass=user.password_hash,
    ):
        raise unauthed_exc

    return user


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=(
            f"invalid token type {current_token_type!r} "
            f"expected {token_type!r}"
        ),
    )
