from datetime import datetime
from random import SystemRandom
from cryptography.fernet import Fernet
import argon2
import jwt
import os

ph = argon2.PasswordHasher()
encryption_key = bytes(os.environ["FERNET_KEY"], encoding="utf-8")

def get_current_isodate(): return datetime.now().isoformat()

def to_jwt(user_id: str):
    fernet = Fernet(encryption_key)
    encrypted_user_id = fernet.encrypt(user_id.encode()).decode()
    
    payload = {"encrypted_id": encrypted_user_id}
    
    secret = os.environ['JWT_SECRET']
    return jwt.encode(payload, secret, algorithm='HS256')

def from_jwt(token: str):
    fernet = Fernet(encryption_key)
    try:
        json_d = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        encrypted_user_id = json_d.get("encrypted_id")
        decrypted_user_id = fernet.decrypt(encrypted_user_id.encode("utf-8")).decode()
        return decrypted_user_id
    except (jwt.DecodeError, jwt.InvalidTokenError) as e:
        print(f"Error decoding token: {str(e)} // Not authenticated?")
        print(f"Token: {token}")
        return None

def hash_password(password): return ph.hash(password) #insert hash function in the future
def verify_hash(hash, password):
    try: return ph.verify(hash, password)
    except argon2.exceptions.VerifyMismatchError: return False
    
def randint_n(d):
    cryptogen = SystemRandom()
    range_start = 10**(d-1)
    range_end = (10**d)-1
    return cryptogen.randint(range_start, range_end)
    
def clean_udata(udata:dict):
    udata.pop("password")
    udata.pop("stripe_id")
    udata.pop("verification_code")
    return udata
    
def is_valid_uuid4(uuid: str):
    if len(uuid) != 36:
        return False

    # All special characters besides '-'
    if any(c in "!@#$%^&*()+?_=,<>/" for c in uuid):
        return False
        
    # Check for 8-4-4-4-12 Constant
    if uuid[8] != '-' or uuid[13] != '-' or uuid[18] != '-' or uuid[23] != '-':
        return False
        
    return True
        
    