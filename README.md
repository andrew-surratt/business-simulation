# Business Simulation

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker with Docker Compose

Install the locked application and test dependencies:

`uv sync --locked --group test`

For a runtime-only environment without coverage or other test tools, use:

`uv sync --locked --no-dev`

## Database

Start PostgreSQL locally:

`docker compose -f compose.yaml up -d`

The application and tests use these defaults:

| Variable | Default |
| --- | --- |
| `POSTGRES_DB` | `business_dashboard` |
| `POSTGRES_USER` | `postgres` |
| `POSTGRES_PASSWORD` | `postgres` |
| `POSTGRES_HOST` | `localhost` |
| `POSTGRES_PORT` | `5432` |

Override them in the environment when needed. CI uses the same PostgreSQL version and settings.

## Test

Run tests:

`uv run --locked manage.py test business`

Run tests with coverage report:

`uv run --locked coverage run manage.py test business && uv run --locked coverage report`

## Start

`uv run --locked python manage.py runserver`

Site is available at http://localhost:8000/

## Migrate DB

If needed, update migrations:

`uv run --locked python manage.py makemigrations`

Run migration:

`uv run --locked python manage.py migrate`

## Admin
Admin site is available at http://localhost:8000/admin/

### Create Admin Superuser

`uv run --locked python manage.py createsuperuser`

### Change Password

`uv run --locked python manage.py changepassword <username>`
