.ONESHELL:

.PHONY: .venv
venv:
	. .venv/bin/activate

.PHONY: start
start: venv
	uvicorn main:app --reload

.PHONY: lint
lint: venv
	mypy main.py

.PHONY: db
db: venv
	docker run -e POSTGRES_PASSWORD=postgres -p 5532:5432 --name borkapi-db -d postgres:16.0

.PHONY: migrate
migrate: venv
	alembic upgrade head

.PHONY: rollback
rollback: venv
	alembic downgrade -1

.PHONY: test
test: venv
	pytest

requirements.txt: venv
	pip freeze >requirements.txt
