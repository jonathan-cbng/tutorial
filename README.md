# Full stack tutorial

This is a full stack application with a Vue.js frontend and a FastAPI backend.

<img width="1768" height="884" alt="image" src="https://github.com/user-attachments/assets/0e1968a7-4b02-4fa5-97dc-843a00cdbec8" />

## Features

- FastAPI backend
- SQLModel ORM with SQLite support
- Modular route structure
- Pytest-based testing suite
- Alembic for database migrations
- Vue.js frontend with Vite

## Running the Application

```shell
python main.py
```

# Development information

## Coding Standards

01. All commit messages must follow conventional-commit rules (<https://www.conventionalcommits.org/en/v1.0.0/#summary>)
02. All code must pass ruff checks (<https://beta.ruff.rs/docs/>), including formatting
03. All code musy conform to the structure of the template files
04. All code must be covered by tests. Coverage must be >90%
05. Python files should be type-annotated as much as possible.
06. Docstring style is Google style (<https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>.
07. Function and method docstrings should have Args, Returns and Raises sections as appropriate.
08. FastAPI endpoints should have fully decorated parameters (e.g. Path, Query, Body etc.) so they render correctly in
    the OpenAPI docs.
09. All files must conform to the template files in the `templates/` directory
10. Max line length is 120 characters for python files.

## Alembic Migrations

To create a new migration after changing the database models, run:

```shell
alembic revision --autogenerate -m "Migration message"
```

To apply migrations, run:

```shell
alembic upgrade head
```

## Running Tests

```shell
python -m pytest test -n4 --cov=backend --cov-report=term-missing
```

## Project Structure

```asciiart
.
├── alembic/                # Database migration files
│   ├── env.py                  # Alembic environment
│   ├── README                  # Alembic documentation
│   ├── script.py.mako          # Alembic script template
│   └── versions/               # Migration versions
├── alembic.ini             # Alembic configuration file
├── app.db                  # SQLite database file for the app (contains standard cases)
├── backend/                # Backend application code
│   ├── api.py                  # FastAPI app factory or main entry point
│   ├── config.py               # App configuration (env vars, settings)
│   ├── db.py                   # Database session and engine setup
│   ├── api_models.py           # Pydantic models for API schemas
│   ├── db_models.py            # SQLModel ORM models for database
│   ├── routes/                 # API route modules
│   │   ├── breed.py                # /breed endpoints
│   │   ├── case.py                 # /case endpoints
│   │   ├── panel.py                # /panel endpoints
│   │   └── sex.py                  # /sex endpoints
│   └── static_data/            # Static data (e.g., dog breeds)
│       └── dog_breeds.py           # List of dog breeds
│       └── clinical_question.py    # Clinical question enums and logic
├── docs/                   # Documentation files
│   └── opeanapi.json          # OpenAPI schema file
├── frontend/               # Frontend application (Vite + Vue)
│   ├── index.html              # Main HTML entry
│   ├── node_modules/           # Node.js dependencies
│   ├── package.json            # Frontend dependencies and scripts
│   ├── package-lock.json       # Lockfile for npm
│   ├── public/                 # Static public assets
│   ├── src/                    # Vue source code
│   └── vite.config.js          # Vite configuration
├── main.py                  # Main entry point: FastAPI app factory, router registration, and Uvicorn startup
├── pyproject.toml           # Project and tool configuration (Ruff, etc.)
├── README.md                # Project documentation
├── requirements-dev.txt     # Development dependencies (pytest, ruff, pre-commit)
├── requirements.txt         # Main Python dependencies
├── run.sh                   # Shell script to run the app
├── templates/               # Template files
│   └── template.py              # Example/template Python file
└── test/                    # Pytest tests and fixtures
    ├── conftest.py              # Test fixtures and setup
    ├── test_breed.py            # Tests for /breeds endpoints
    ├── test_case.py             # Tests for /case endpoints
    ├── test_root.py             # Tests for /api root endpoint
    └── test_sex.py              # Tests for /sex endpoints
```

## Backend API summary

Below is a list of the main API endpoints provided by the FastAPI backend.

### Root

- `GET /api/` — Root endpoint providing basic API information.

### Animal Information

- `GET /api/breed` — List all breeds (optionally filter by species)
- `GET /api/breed/{breed_id}` — Retrieve a breed by ID
- `GET /api/breed/by_name/{breed_name}` — Retrieve a breed by name
- `GET /api/species` — List all possible animal species
- `GET /api/sex` — List all possible animal sexes

### Cases

- `GET /api/case` — List all clinical cases
- `POST /api/case` — Create a new clinical case
- `GET /api/case/{case_id}` — Retrieve a clinical case by ID
- `PUT /api/case/{case_id}` — Update a clinical case by ID
- `DELETE /api/case/{case_id}` — Delete a clinical case by ID
