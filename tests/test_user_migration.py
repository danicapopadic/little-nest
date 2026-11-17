import importlib.util
from pathlib import Path
from types import ModuleType

from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, inspect


def _load_migration() -> ModuleType:
    path = (
        Path(__file__).resolve().parents[1]
        / "alembic"
        / "versions"
        / "b7e4d1a9c2f0_create_users_table.py"
    )
    spec = importlib.util.spec_from_file_location("create_users_table", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_users_migration_creates_and_drops_table() -> None:
    migration = _load_migration()
    engine = create_engine("sqlite://")

    with engine.begin() as connection:
        context = MigrationContext.configure(connection)
        with Operations.context(context):
            migration.upgrade()

        inspector = inspect(connection)
        assert "users" in inspector.get_table_names()

        columns = {column["name"]: column for column in inspector.get_columns("users")}
        assert columns["name"]["nullable"] is False
        assert columns["email"]["nullable"] is False
        assert columns["password_hash"]["nullable"] is False

        unique_constraints = inspector.get_unique_constraints("users")
        assert any(
            constraint["column_names"] == ["email"] for constraint in unique_constraints
        )

        with Operations.context(context):
            migration.downgrade()

        assert "users" not in inspect(connection).get_table_names()
