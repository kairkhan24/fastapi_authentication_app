from src.domain import service
from src.domain.exceptions import EmailTaken, UsernameTaken
from src.domain.schemas import RegisterUser


async def valid_user_create(user: RegisterUser) -> RegisterUser:
    if await service.get_user_by_username(user.username):
        raise UsernameTaken()

    if await service.get_user_by_email(user.email):
        raise EmailTaken()

    return user
