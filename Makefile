start:
	uvicorn main:app --reload

db:
	docker run -e POSTGRES_PASSWORD=postgres -p 5532:5432 --name borkapi-db -d postgres:16.0

migrate:
	alembic upgrade head