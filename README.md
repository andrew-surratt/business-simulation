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

| Variable            | Default              | Description                                            |
|---------------------|----------------------|--------------------------------------------------------|
| `POSTGRES_DB`       | `business_dashboard` | Postgres DB                                            |
| `POSTGRES_USER`     | `postgres`           | Postgres User                                          |
| `POSTGRES_PASSWORD` | None                 | (Required) Postgres Password                           |
| `POSTGRES_HOST`     | `localhost`          | Postgres Host                                          |
| `POSTGRES_PORT`     | `5432`               | Postgres Port                                          |
| `DJANGO_SECRET_KEY` | None                 | (Required) Django Secret Key for cryptographic signing |

Override them in the environment when needed. **For production deployments, always set `POSTGRES_PASSWORD` and `SECRET_KEY` as environment variables.**

### Setting Environment Variables

Create a `.env` file or export variables in your shell:

```bash
DJANGO_SECRET_KEY='your-secret-key-here'
POSTGRES_PASSWORD='your-secure-password'
POSTGRES_HOST='your-db-host'
POSTGRES_USER='your-db-user'
```

Then run:

```bash
uv run --locked python manage.py runserver
```

### GitHub Actions Secrets

For CI/CD, add these secrets to your repository settings:

1. Go to **Settings > Secrets and variables > Actions**
2. Click **New repository secret**
3. Add the following secrets:
   - `DJANGO_SECRET_KEY` - A secure Django secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `POSTGRES_PASSWORD` - Your test database password

## Test

To run only the unit tests without PostgreSQL, or Docker:

`make test-unit`

Before opening a pull request, start PostgreSQL and run the complete unit and integration suite:

```shell
docker compose up -d postgres
make test
```

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
