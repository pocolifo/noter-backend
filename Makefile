init:
	pip install -r requirements.txt
	cd backend && alembic upgrade head
	cat "\n" >> .env
	cat .env.default >> .env

run:
	uvicorn backend:app --host 0.0.0.0 --port 8000 --env-file .env &
		uvicorn meta:app --host 0.0.0.0 --port 9000 --env-file .env

test:
	pytest
