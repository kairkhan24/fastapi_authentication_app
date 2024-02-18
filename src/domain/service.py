from datetime import datetime
from typing import Any

from sqlalchemy import insert, select

from src.domain.exceptions import InvalidCredentials, UserNotFound
from src.domain.schemas import AuthUser, RegisterUser
from src.domain.utils import check_password, hash_password
from src.infrastructure.database import auth_user, fetch_one


async def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    select_query = select(auth_user).where(auth_user.c.id == user_id)
    user = await fetch_one(select_query)
    if user is None:
        raise UserNotFound()

    return user


async def get_user_by_username(username: str) -> dict[str, Any] | None:
    select_query = select(auth_user).where(auth_user.c.username == username)
    return await fetch_one(select_query)


async def get_user_by_email(user_email: str) -> dict[str, Any] | None:
    select_query = select(auth_user).where(auth_user.c.email == user_email)
    return await fetch_one(select_query)


async def authenticate_user(auth_data: AuthUser) -> dict[str, Any]:
    user = await get_user_by_username(auth_data.username)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    return user


async def create_user(user: RegisterUser) -> dict[str, Any] | None:
    insert_query = (
        insert(auth_user)
        .values(
            {
                "username": user.username,
                "email": user.email,
                "password": hash_password(user.password),
                "created_at": datetime.utcnow(),
            }
        )
        .returning(auth_user)
    )

    return await fetch_one(insert_query)
