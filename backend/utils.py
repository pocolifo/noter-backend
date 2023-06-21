from datetime import datetime

def get_current_isodate(): return str(datetime.now().isoformat())
def hash_password(password): return password #insert hash function in the future