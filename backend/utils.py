from datetime import datetime
from globals import *
import argon2, jwt

ph = argon2.PasswordHasher()

def get_current_isodate(): return str(datetime.now().isoformat())

def to_jwt(id:str): # User ID -> Encrypted JSON
    data = {"id":id}
    secret = JWT_SECRET()
    return str(jwt.encode(data, secret, algorithm='HS256'))
    
def from_jwt(wt:str): # Encrypted JSON -> User ID
    try:
        json_d = jwt.decode(wt, JWT_SECRET(), algorithms=['HS256'])
        return json_d.get("id")
    except jwt.DecodeError as e:
        print(f"Error decoding token: {str(e)} // Not authenticated?")
        print(f"Token: {wt}")
        return None

def hash_password(password): return ph.hash(password) #insert hash function in the future
def verify_hash(hash, password):
    try: return ph.verify(hash, password)
    except argon2.exceptions.VerifyMismatchError: return False