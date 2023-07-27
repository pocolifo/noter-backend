init:
	pip install -r requirements.txt
	cd backend
	alembic upgrade head
	cd ..

run:
	uvicorn backend:app

test:
	pytest