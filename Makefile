init:
	pip install -r requirements.txt
	cd backend && alembic upgrade head

run:
	uvicorn backend:app

test:
	pytest