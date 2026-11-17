from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from little_nest.models import Base, User
from little_nest.schemas import UserResponse


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as db_session:
        yield db_session


def test_user_can_be_created_and_queried(session: Session) -> None:
    user = User(
        name="Ada Lovelace",
        email="ada@example.com",
        password_hash="hashed-password",
    )
    session.add(user)
    session.commit()

    found = session.scalars(select(User).where(User.email == "ada@example.com")).one()

    assert found.id is not None
    assert found.name == "Ada Lovelace"
    assert found.email == "ada@example.com"
    assert found.password_hash == "hashed-password"
    assert found.created_at is not None
    assert found.updated_at is not None


def test_name_is_required(session: Session) -> None:
    session.add(User(email="ada@example.com", password_hash="hashed-password"))

    with pytest.raises(IntegrityError):
        session.commit()


def test_email_is_required(session: Session) -> None:
    session.add(User(name="Ada Lovelace", password_hash="hashed-password"))

    with pytest.raises(IntegrityError):
        session.commit()


def test_password_hash_is_required(session: Session) -> None:
    session.add(User(name="Ada Lovelace", email="ada@example.com"))

    with pytest.raises(IntegrityError):
        session.commit()


def test_email_is_unique(session: Session) -> None:
    session.add(User(name="Ada Lovelace", email="ada@example.com", password_hash="one"))
    session.commit()
    session.add(User(name="Ada Lovelace", email="ada@example.com", password_hash="two"))

    with pytest.raises(IntegrityError):
        session.commit()


def test_password_hash_is_not_exposed_in_api_responses(session: Session) -> None:
    user = User(
        name="Ada Lovelace",
        email="ada@example.com",
        password_hash="hashed-password",
    )
    session.add(user)
    session.commit()

    payload = UserResponse.model_validate(user).model_dump()

    assert payload["name"] == "Ada Lovelace"
    assert payload["email"] == "ada@example.com"
    assert "password_hash" not in payload
    assert "password" not in payload
    assert "hashed-password" not in repr(user)
