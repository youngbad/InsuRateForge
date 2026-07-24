from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_register_login_and_me(client) -> None:
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "customer@example.com",
            "full_name": "Customer Example",
            "password": "StrongPass123",
            "roles": ["admin"],
        },
    )
    assert register_response.status_code == 201
    registered = register_response.json()
    assert registered["email"] == "customer@example.com"
    assert registered["roles"] == ["customer"]

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "customer@example.com", "password": "StrongPass123"},
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert tokens["token_type"] == "bearer"
    assert tokens["access_token"]
    assert tokens["refresh_token"]

    me_response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer " + tokens["access_token"]},
    )
    assert me_response.status_code == 200
    me = me_response.json()
    assert me["email"] == "customer@example.com"
    assert me["roles"] == ["customer"]

    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refresh_response.status_code == 200
    assert refresh_response.json()["access_token"]


@pytest.mark.asyncio
async def test_customer_cannot_list_users(client) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "another@example.com",
            "full_name": "Another Customer",
            "password": "StrongPass123",
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "another@example.com", "password": "StrongPass123"},
    )
    token = login_response.json()["access_token"]
    users_response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": "Bearer " + token},
    )
    assert users_response.status_code == 403
