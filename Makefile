deps:
	echo "installing dependencies for debian"
	sudo apt install python3-pip postgresql postgresql-client -y
	sudo runuser postgres -c 'cd && createdb noter && psql noter -c "ALTER USER postgres WITH PASSWORD \'1234\';"'
	
	cat <<'EOF' >.env
	SQLALCHEMY_URL="postgresql://postgres:1234@localhost:5432/noter"
	EOF

init:
	pip install -r requirements.txt

	touch .env
	cp .env.default .env.tmp
	cat .env >> .env.tmp
	mv .env.tmp .env

	cd backend && alembic upgrade head

run:
	uvicorn backend:app --host 0.0.0.0 --port 8000 --env-file .env &
		uvicorn meta:app --host 0.0.0.0 --port 9000 --env-file .env

test:
	pytest
