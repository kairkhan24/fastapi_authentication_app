from pydantic import BaseModel, EmailStr, Field


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class AuthUser(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=128)


class RegisterUserResponse(BaseModel):
    success: bool
    user_id: int


class AuthUserResponse(BaseModel):
    success: bool
    access_token: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr


class JWTData(BaseModel):
    user_id: int = Field(alias="sub")
