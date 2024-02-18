import pytest
from async_asgi_testclient import TestClient
from fastapi import status


@pytest.mark.asyncio
async def test_register_success(client: TestClient) -> None:
    resp = await client.post(
        "/api/users/register",
        json={
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "zxc123!Q",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json['success']


@pytest.mark.asyncio
async def test_register_email_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.domain.dependencies import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_email", fake_getter)

    resp = await client.post(
        "/api/users/register",
        json={
            "username": "testuser12",
            "email": "test@gmail.com",
            "password": "zxc123!Q",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp_json["detail"] == 'Email is already taken.'


@pytest.mark.asyncio
async def test_register_username_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.domain.dependencies import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_username", fake_getter)

    resp = await client.post(
        "/api/users/register",
        json={
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "zxc123!Q",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp_json["detail"] == 'Username is already taken.'


@pytest.mark.asyncio
async def test_authenticate_user_success(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.domain.dependencies import service

    async def fake_user(*args, **kwargs):
        return {'id': 1, 'password': '123'}

    def fake_check_password(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_username", fake_user)
    monkeypatch.setattr(service, "check_password", fake_check_password)

    resp = await client.post(
        "/api/users/auth",
        json={
            "username": "testuser",
            "password": "zxc123!Q",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json["success"]


@pytest.mark.asyncio
async def test_authenticate_invalid_username(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.domain.dependencies import service

    async def fake_user(*args, **kwargs):
        return False

    def fake_check_password(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_username", fake_user)
    monkeypatch.setattr(service, "check_password", fake_check_password)

    resp = await client.post(
        "/api/users/auth",
        json={
            "username": "testuser34",
            "password": "zxc123!Q",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp_json["detail"] == 'Invalid credentials.'


@pytest.mark.asyncio
async def test_authenticate_invalid_password(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.domain.dependencies import service

    async def fake_user(*args, **kwargs):
        return {'id': 1, 'password': '123456'}

    def fake_check_password(*args, **kwargs):
        return False

    monkeypatch.setattr(service, "get_user_by_username", fake_user)
    monkeypatch.setattr(service, "check_password", fake_check_password)

    resp = await client.post(
        "/api/users/auth",
        json={
            "username": "testuser34",
            "password": "zxc123!Q",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp_json["detail"] == 'Invalid credentials.'
