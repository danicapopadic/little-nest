# Little Nest

Household management application built with Python.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python dependency management

## Local setup

1. Clone the repository and navigate to the project directory.
2. Install the project and its dependencies:

   ```bash
   uv sync
   ```

3. Verify the installation:

   ```bash
   uv run python -c "import little_nest; print('Package import OK')"
   ```

`uv sync` automatically creates a virtual environment in `.venv/` and installs the project.

You don't need to activate the virtual environment manually when using `uv run`.

## Project structure

```text
little-nest/
├── src/
│   └── little_nest/
│       └── __init__.py
├── .gitignore
├── .python-version
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

## Code Reviews

Little Nest uses [CodeRabbit](https://www.coderabbit.ai/) for AI-assisted pull request reviews.

Review behavior is configured in [`.coderabbit.yaml`](.coderabbit.yaml), with a focus on Python correctness, security, maintainability, and testing.

**Note:** CodeRabbit currently requires manual review triggering because the repository has fewer than 10 GitHub stars. Reviews can be requested through the **Trigger review** option on a pull request.

CodeRabbit feedback is advisory. All suggestions should be evaluated before implementation, and AI reviews do not replace automated tests or developer judgment. Invalid or irrelevant suggestions may be dismissed with an explanation.

CodeRabbit has repository access through its GitHub App. Review permissions and plan or billing limits should be checked in CodeRabbit before making changes.

## Running the API locally

Start the development server:

```bash
uv run uvicorn little_nest.main:app --reload
```

The API is available at http://127.0.0.1:8000.

- Health check: `/health`
- API documentation: `/docs`

## Running tests

Run the automated test suite:

```bash
uv run pytest
```