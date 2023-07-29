from fastapi.testclient import TestClient
from backend.environment import load_all, append_to_environ
append_to_environ(load_all())

from backend.app import app
from backend.noterdb import db

# Create test client and connect to DB
client = TestClient(app=app)

# Create a test user
TEST_USER_EMAIL = 'test@example.com'
TEST_USER_PASSWORD = 'test'
