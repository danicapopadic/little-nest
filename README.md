# Little Nest

A household management application built with Python.

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