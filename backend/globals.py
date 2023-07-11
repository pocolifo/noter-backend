import os

def CONN_LINK() -> str:
    if 'SQLALCHEMY_URL' in os.environ:
        return os.environ['SQLALCHEMY_URL']
    else:
        return "postgresql://postgres:password@localhost/postgres" # Assumes Port is Default (5432)

def API_VERSION() -> float: return 1.1
def JWT_SECRET() -> str: return "secret_key"
def CORS_ALLOW_ORIGINS() -> list[str]: return os.environ.get('CORS_ALLOW_ORIGINS', 'http://localhost:5173').split(',')
