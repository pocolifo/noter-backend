import pytest, asyncio

from .context import db, client, TEST_USER_EMAIL, TEST_USER_PASSWORD
from backend.tables import User
from backend.make_objects import make_user
from backend.utils import hash_password

def pytest_sessionstart():
    print('Session starting... creating test user.')
    user = make_user(TEST_USER_EMAIL, hash_password(TEST_USER_PASSWORD))
    
    loop = asyncio.new_event_loop() # This function cannot be asynchronous but must await the insert user function. Asyncio event loop instead of 'await'
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db.user_manager.insert(user))
    loop.close()
    
    print('Created test user successfully.')


@pytest.fixture(autouse=True)
def clear_cookies():
    client.cookies.clear()

def pre_authenticate(func):
    def wrapper():
        client.post('/authenticate', json={'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
        func()
    
    return wrapper