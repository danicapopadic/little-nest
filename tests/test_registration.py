from fastapi.testclient import TestClient
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from little_nest.models import User


def test_successful_registration(
    registration_client: TestClient,
    postgres_session: Session,
) -> None:
    password = "TestPassword123"

    response = registration_client.post(
        "/auth/register",
        json={
            "name": "Ada Lovelace",
            "email": "Ada@example.com",
            "password": password,
        },
    )

    assert response.status_code == 201

    payload = response.json()

    assert payload["name"] == "Ada Lovelace"
    assert payload["email"] == "ada@example.com"
    assert "password" not in payload
    assert "password_hash" not in payload

    user = postgres_session.scalars(
        select(User).where(User.email == "ada@example.com")
    ).one()

    assert user.id == payload["id"]
    assert user.password_hash != password
    assert user.password_hash.startswith("$argon2id$")
    assert PasswordHash.recommended().verify(password, user.password_hash)


def test_duplicate_email_is_rejected(
    registration_client: TestClient,
) -> None:
    data = {
        "name": "Ada Lovelace",
        "email": "Ada@example.com",
        "password": "TestPassword123",
    }

    first_response = registration_client.post("/auth/register", json=data)

    assert first_response.status_code == 201

    data["email"] = "ada@example.com"

    second_response = registration_client.post("/auth/register", json=data)

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Email already registered",
    }


def test_invalid_registration_data_is_rejected(
    registration_client: TestClient,
) -> None:
    response = registration_client.post(
        "/auth/register",
        json={
            "name": "",
            "email": "invalid-email",
            "password": "123",
        },
    )

    assert response.status_code == 422

    errors = response.json()["detail"]
    fields = {error["loc"][-1] for error in errors}

    assert fields == {"name", "email", "password"}
    assert all("input" not in error for error in errors)
    assert all("ctx" not in error for error in errors)
    assert "123" not in response.text


def test_name_with_nul_character_is_rejected(
    registration_client: TestClient,
) -> None:
    response = registration_client.post(
        "/auth/register",
        json={
            "name": "Ada\x00",
            "email": "ada@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "name"]


def test_unicode_name_is_accepted(
    registration_client: TestClient,
) -> None:
    response = registration_client.post(
        "/auth/register",
        json={
            "name": "Petar Petrović",
            "email": "petar@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Petar Petrović"
