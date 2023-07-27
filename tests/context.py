from fastapi.testclient import TestClient

import backend
from backend.noterdb import DB
from backend.globals import CONN_LINK

# Create test client and connect to DB
client = TestClient(app=backend.app)
db = DB(CONN_LINK())
assert db.connect()

# Create a test user
TEST_USER_EMAIL = 'test@example.com'
TEST_USER_PASSWORD = 'test'
