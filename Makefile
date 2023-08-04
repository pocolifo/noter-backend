init:
	pip install -r requirements.txt
	cd backend && alembic upgrade head

	cp .env.default .env.tmp
	cat .env >> .env.tmp
	mv .env.tmp .env

run:
	uvicorn backend:app --host 0.0.0.0 --port 8000 --env-file .env &
		uvicorn meta:app --host 0.0.0.0 --port 9000 --env-file .env

test:
	pytest
