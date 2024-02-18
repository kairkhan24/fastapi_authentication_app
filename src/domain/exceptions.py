from typing import Any

from fastapi import HTTPException as _HTTPException
from fastapi import status


class HTTPException(_HTTPException):
    STATUS_CODE = None
    DETAIL = None

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class AuthRequired(HTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Auth is required.'


class AuthorizationFailed(HTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = 'Authorization failed.'


class InvalidToken(HTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Invalid token.'


class InvalidCredentials(HTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'Invalid credentials.'


class EmailTaken(HTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Email is already taken.'


class UserNotFound(HTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = 'User not found.'


class UsernameTaken(HTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Username is already taken.'
