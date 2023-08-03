from dotenv import load_dotenv
load_dotenv()

from fastapi.testclient import TestClient

from backend.app import app
from backend.noterdb import db


# Create test client and connect to DB
client = TestClient(app=app)

# Create a test user
TEST_USER_EMAIL = 'test@example.com'
TEST_USER_PASSWORD = 'test'
