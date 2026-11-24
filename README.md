# Little Nest

Household management application built with Python.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python dependency management
- Docker Desktop for the containerized development environment

## Local setup

1. Clone the repository and navigate to the project directory.
2. Install the project and its dependencies:

   ```bash
   uv sync
   ```

3. Create a local environment configuration:

   ```bash
   cp .env.example .env
   ```

4. Verify the installation:

   ```bash
   uv run python -c "import little_nest; print('Package import OK')"
   ```

`uv sync` automatically creates a virtual environment in `.venv/` and installs the project.

You don't need to activate the virtual environment manually when using `uv run`.

## Project structure

```text
little-nest/
├── alembic/
│   ├── versions/
│   └── env.py
├── src/
│   └── little_nest/
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       ├── services/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── main.py
│       └── security.py
├── tests/
│   ├── conftest.py
│   ├── test_database.py
│   ├── test_health.py
│   ├── test_registration.py
│   └── test_security.py
├── .env.example
├── .gitignore
├── .python-version
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Dependency management

Add a project dependency:

```bash
uv add package-name
```

Add a development dependency:

```bash
uv add --dev package-name
```

Synchronize the environment:

```bash
uv sync
```

Dependencies are defined in `pyproject.toml`, and exact resolved versions are recorded in `uv.lock`.

Both files should be committed to Git.

## Running the API locally

Start the development server:

```bash
uv run uvicorn little_nest.main:app --reload
```

The API is available at http://127.0.0.1:8000.

The application requires a valid `DATABASE_URL` pointing to an accessible PostgreSQL database.

The development PostgreSQL container does not expose its port to the host. For a complete development environment, use Docker Compose as described below.

## Docker development environment

The development environment uses Docker Compose to run FastAPI and PostgreSQL.

### Setup

1. Install Docker Desktop.
2. Create a `.env` file if one does not already exist:

   ```bash
   cp .env.example .env
   ```

3. Set your local `POSTGRES_PASSWORD` in `.env`.
4. Build and start the development services:

   ```bash
   docker compose up --build -d api db
   ```

5. Apply database migrations:

   ```bash
   docker compose exec api uv run --no-sync alembic upgrade head
   ```

### Automatic reload

The API container mounts the local `src/` directory and uses Uvicorn's automatic reload feature.

Changes to Python source files are automatically reflected in the running application without rebuilding the Docker image.

Rebuild the API image when dependencies or the Dockerfile change:

```bash
docker compose up --build -d api
```

Automatic reload is configured in Docker Compose for development only.

### Useful commands

| Command | Description |
|---|---|
| `docker compose ps` | Check container status |
| `docker compose logs -f api` | View API logs |
| `docker compose logs -f db` | View database logs |
| `docker compose stop` | Stop services |
| `docker compose up -d api db` | Start development services |
| `docker compose up --build -d api db` | Rebuild and start development services |
| `docker compose down` | Remove containers and network, preserving persistent database data |

### Access

- API: http://localhost:8000
- Health check: http://localhost:8000/health
- API documentation: http://localhost:8000/docs

Development PostgreSQL data is stored in a persistent Docker volume.

**Important:** Avoid `docker compose down -v` unless you intentionally want to delete the database volume and its data.

The `.env` file contains local credentials and must never be committed to Git.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| POST | `/auth/register` | Register a new user |

### User registration

Example request:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "password": "ExamplePassword123"
  }'
```

Registration validates the submitted data, normalizes email addresses to lowercase, rejects duplicate emails, and hashes passwords using Argon2id.

Passwords and password hashes are not included in API responses.

| Status code | Description |
|---|---|
| 201 Created | Successful registration |
| 409 Conflict | Email already registered |
| 422 Unprocessable Entity | Invalid request data |

## Database & Migrations

Little Nest uses PostgreSQL for data storage, SQLAlchemy for database access, and Alembic for schema migrations.

Database migrations run inside the API container, which connects to PostgreSQL using the Docker Compose service hostname `db`.

Unique constraints follow the centralized SQLAlchemy naming convention `uq_<table_name>_<column_name>`.

### Creating migrations

Create a new migration:

```bash
docker compose exec api uv run --no-sync alembic revision -m "description"
```

Migration files are automatically synchronized to the local `alembic/versions/` directory.

### Applying migrations

Apply all pending migrations:

```bash
docker compose exec api uv run --no-sync alembic upgrade head
```

Check the currently applied migration:

```bash
docker compose exec api uv run --no-sync alembic current
```

### Rolling back migrations

Roll back the most recent migration:

```bash
docker compose exec api uv run --no-sync alembic downgrade -1
```

**Important:** Review migrations before applying them, especially when modifying or removing existing database columns or tables.

## Running tests

The project uses Pytest for automated testing, including unit tests and PostgreSQL integration tests.

Registration tests use a dedicated PostgreSQL instance to verify database persistence, password hashing, email uniqueness, and request validation.

### Test database setup

Ensure the following variable is configured in your local `.env`:

```dotenv
TEST_DATABASE_URL=postgresql+psycopg://test:test@localhost:5433/little_nest_test
```

Start the test database:

```bash
docker compose up -d db_test
```

Verify that PostgreSQL is ready:

```bash
docker compose exec db_test pg_isready -U test -d little_nest_test
```

### Running the test suite

Run all tests:

```bash
DATABASE_URL="$(
  grep '^TEST_DATABASE_URL=' .env | cut -d= -f2-
)" uv run pytest
```

Run registration tests only:

```bash
DATABASE_URL="$(
  grep '^TEST_DATABASE_URL=' .env | cut -d= -f2-
)" uv run pytest tests/test_registration.py -v
```

The API container and development database do not need to be running.

### Test database isolation

The test database:

- Runs in a separate PostgreSQL 17 container.
- Uses host port `5433`.
- Uses temporary storage instead of a persistent volume.
- Creates and removes test tables through pytest fixtures.
- Is isolated from the development database.

The PostgreSQL test fixture requires the database name to be `little_nest_test` as an additional safety measure.

Integration tests create tables from SQLAlchemy metadata rather than applying Alembic migrations.

Stop the test database when finished:

```bash
docker compose stop db_test
```

## Code quality checks

The project uses **Ruff** for linting and formatting, **Pyright** for type checking, and **Pytest** for automated tests.

### Local checks

Run all pre-commit checks:

```bash
uv run pre-commit run --all-files
```

Individual checks can also be run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

Automatically format code:

```bash
uv run ruff format .
```

Run