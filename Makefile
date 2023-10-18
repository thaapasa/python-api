.PHONY: start
start:
	poetry run uvicorn main:app --reload

.PHONY: lint
lint:
	poetry run mypy main.py

.PHONY: db
db: venv
	docker run -e POSTGRES_PASSWORD=postgres -p 5532:5432 --name borkapi-db -d postgres:16.0

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: rollback
rollback:
	poetry run alembic downgrade -1

.PHONY: test
test:
	poetry run pytest

.PHONE: install
install:
	poetry install
