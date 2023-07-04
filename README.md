# Setup
### Once you've setup an empty PostgreSQL database and it's running on your localhost:


1. Open `backend/alembic.ini` and assign the `sqlalchemy.url` variable (line 63) to your database connection URL. Your connection URL will be in the following format: `postgresql://DB_USER:DB_PASS@DB_HOST/DB_NAME`
Replace DB_USER, DB_PASS, DB_HOST and DB_NAME to the values that suit your database.
**Note:** *Since there isn't a specified port in the URL it will assume the port is 5432, the default port for PostgreSQL. If you configured a different port then append `:PORT` to DB_HOST replacing PORT with your port number.*

2. Open a terminal in the `backend` directory and execute `alembic upgrade head` to create all the necessary data structures in your database.

3. Open `backend/globals.py` and edit the return value of the `CONN_LINK()` function. Change this return value to the same value you set `sqlalchemy.url` to in step 1.

4. Run the main file by using the command `uvicorn main:app` in the `backend` directory. By default it will run on localhost:8000 but you can change the host and port with flags `--host` and `--port`.

5. Good job! Now the backend is running properly.
