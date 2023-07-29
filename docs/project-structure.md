# Project structure

## `admin/`
- Admin dashboard to administrate the database and backend app
- Uses `starlette-admin`

## `backend/`
- The Noter backend API itself
- Uses FastAPI, SQLAlchemy, OpenAI, Stripe

## `backend/alembic`
- Alembic database migrations for the Noter API database
- Uses Alembic

## `docs/`
- Documentation markdown files

## `tests/`
- Tests for the Noter API (not the admin dashboard)
- Uses `pytest`
- `tests/conftest.py` cannot be renamed, it is a reserved file name for pytest
- Create tests by
    - adding a Python file if necessary with the topic of the tests prefixed by `test_` OR find a pre-existing file with the kind of tests you're looking for
    - then add a test by making a function called whatever it tests prefixed by `test_`
        - if it requires user authentication, decorate it with `@pre_authenticate`

