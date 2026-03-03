# Contributing

## Prerequisites

- **Python >=3.13+**
- **[uv](https://docs.astral.sh/uv/)** — Python package and project manager

## Setup

Clone the repo and install dependencies:

```bash
git clone git@github.com:cylf-dev/chunk-utils.git
cd chunk-utils
uv sync --locked
```

This creates a virtualenv in `.venv/` and installs all dependencies (including dev tools).

Set up pre-commit hooks:

```bash
uv run pre-commit install
```

## Running tests

```bash
uv run pytest tests/ -v
```

## Linting and formatting

Ruff is used for both linting and formatting:

```bash
uv run ruff check .
uv run ruff format .
```

Type checking:

```bash
uv run mypy src/
```

Pre-commit runs all of these automatically on staged files.

## Versioning

This project uses **dynamic versioning** based on git tags. The version is automatically derived from the repository state:

- **Tagged commits** (e.g., `v0.1.0`) produce exact versions: `0.1.0`
- **Commits after a tag** produce development versions with git metadata: `0.1.1.dev3+g1a2b3c4`
  - `.dev3` indicates 3 commits since the last tag
  - `+g1a2b3c4` includes the abbreviated git SHA

This follows [PEP 440](https://peps.python.org/pep-0440/) and [Semantic Versioning](https://semver.org/).

**Tag format**: Use `v` prefix followed by semantic version: `v0.1.0`, `v1.0.0`, `v1.2.3`

You can check the current version:

```bash
python -c "from chunk_utils import __version__; print(__version__)"
```
