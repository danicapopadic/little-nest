import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from little_nest.database import get_db
from little_nest.main import app
from little_nest.models import Base

load_dotenv()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def postgres_session() -> Iterator[Session]:
    url = make_url(os.environ["TEST_DATABASE_URL"])

    if url.database != "little_nest_test":
        raise RuntimeError("Unsafe test database name")

    engine = create_engine(url)

    try:
        Base.metadata.create_all(engine)
        factory = sessionmaker(bind=engine)

        with factory() as session:
            yield session
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def registration_client(
    postgres_session: Session,
) -> Iterator[TestClient]:
    def override_get_db() -> Iterator[Session]:
        yield postgres_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
