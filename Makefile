.PHONY: test-unit test

# Local development shortcut: uses the existing environment and no services.
test-unit:
	uv run --locked --no-sync python manage.py test business.tests.unit

# Authoritative final check used locally and in CI. PostgreSQL must be running.
test:
	uv run --locked coverage erase
	uv run --locked coverage run manage.py test business.tests
	uv run --locked coverage report

