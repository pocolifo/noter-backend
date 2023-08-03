init:
	pip install -r requirements.txt
	cd backend && alembic upgrade head
	cp .env.default .env

run:
	uvicorn admin:app --host 127.0.0.1 --port 7000 --env-file .env &
		uvicorn backend:app --host 0.0.0.0 --port 8000 --env-file .env &
		uvicorn meta:app --host 0.0.0.0 --port 9000 --env-file .env

test:
	pytest