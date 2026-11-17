from contextlib import suppress
from unittest.mock import MagicMock, patch

from little_nest.database import get_db


def test_get_db_closes_session():
    mock_session = MagicMock()
    mock_session.__enter__.return_value = mock_session

    with patch("little_nest.database.SessionLocal", return_value=mock_session):
        db = get_db()

        assert next(db) is mock_session

        with suppress(StopIteration):
            next(db)

        mock_session.__exit__.assert_called_once()
