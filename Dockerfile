FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY README.md ./
COPY src/ ./src/
COPY alembic.ini ./
COPY alembic/ ./alembic/

RUN uv sync --locked --no-dev

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "little_nest.main:app", "--host", "0.0.0.0", "--port", "8000"]