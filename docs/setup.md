# Set up the Noter API

## 1. Requirements

- PostgreSQL server
- Python 3.8+ and PIP
- Make

## 2. Environment variables

- Set through a `.env` file or any other way to set an environment variable
- You'll need to set the **`SQLALCHEMY_URL` variable to your database URL**
    - Set it to `postgresql://username:password@host:port/database` where 
        - `username` is the user to connect to the database with
        - `password` is the password of that user
        - `host` is the host of the database (i.e. IP address, domain name like `127.0.0.1` or `postgres.getnoter.com`)
        - `port` is the integer port to connect to on the host. It defaults to `5432` if not set.
        - `database` is the database on the PostgreSQL server to use

### 2.1 All environment variables

| Variable           | Value                                                        |
|--------------------|--------------------------------------------------------------|
| STRIPE_API_KEY     | The Stripe secret key                                        |
| OPENAI_API_KEY     | The OpenAI key to use for AI endpoints                       |
| SQLALCHEMY_URL     | The database connection URL for Postgres                     |
| SMTP_SERVER        | The SMTP server host                                         |
| SMTP_PORT          | The SMTP port of the server                                  |
| SMTP_ADDRESS       | The email to use on the SMTP server                          |
| SMTP_PASSWORD      | The password for the SMTP user                               |
| JWT_SECRET         | The JSON web token secret key                                |
| CORS_ALLOW_ORIGINS | The origins to set in the Access-Control-Allow-Origin header |

## 3. Makefile

- Initialize your development environment: `make init`.
- Run the backend: `make run`
- Test the backend (**you need a clean database each time**):  `make test`