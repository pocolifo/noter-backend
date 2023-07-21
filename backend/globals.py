import os
from typing import List
import stripe

def CONN_LINK() -> str:
    if 'SQLALCHEMY_URL' in os.environ:
        return os.environ['SQLALCHEMY_URL']
    else:
        return "postgresql://postgres:ilovebigblackcock69@localhost/postgres2" # Assumes Port is Default (5432)

def SMTP_LOGIN() -> dict:
    return {
    "server":"smtp.gmail.com",
    "port":587,
    "email":"jayfishman98@gmail.com",
    "password":"zwnzditfpwtzubsm"
    }
    
def API_VERSION() -> float: return 1.1
def JWT_SECRET() -> str: return "secret_key"
def CORS_ALLOW_ORIGINS() -> List[str]: return os.environ.get('CORS_ALLOW_ORIGINS', 'http://localhost:5173').split(',')

stripe.api_key = "sk_test_51N07ZAExIIMbGntrafqnAjdH5Gym0q2N8yL5ui6CvTDzJK0Bz4Z5fIgxamI99i264i1md7irzRsYeDbNOesNtvFy00qFgtNMDC"
#stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')