from datetime import datetime
import argon2

ph = argon2.PasswordHasher()

def get_current_isodate(): return str(datetime.now().isoformat())
def hash_password(password): return ph.hash(password) #insert hash function in the future
def verify_hash(hash, password):
    print(hash)
    try: return ph.verify(hash, password)
    except argon2.exceptions.VerifyMismatchError: return False