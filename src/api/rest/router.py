from fastapi import APIRouter, Depends, status

from src.domain import service
from src.domain.dependencies import valid_user_create
from src.domain.jwt import create_access_token, parse_jwt_user_data
from src.domain.schemas import (AuthUser, AuthUserResponse, JWTData,
                                RegisterUser, RegisterUserResponse,
                                UserResponse)

router = APIRouter()


@router.post('/users/register', status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse)
async def register_user(
    register_data: RegisterUser = Depends(valid_user_create)
):
    user = await service.create_user(register_data)
    return RegisterUserResponse(success=True, user_id=user['id'])


@router.post('/users/auth', status_code=status.HTTP_200_OK, response_model=AuthUserResponse)
async def auth_user(auth_data: AuthUser) -> AuthUserResponse:
    user = await service.authenticate_user(auth_data)
    access_token = create_access_token(user=user)
    return AuthUserResponse(success=True, access_token=access_token)


@router.get("/users/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> UserResponse:
    user = await service.get_user_by_id(jwt_data.user_id)
    return UserResponse(username=user['username'], email=user['email'])
