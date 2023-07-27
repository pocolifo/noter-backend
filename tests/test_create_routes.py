from .conftest import pre_authenticate
from .context import client

import uuid


def test_create_account():
    EMAIL = 'example@example.com'
    PASSWORD = 'example'

    response = client.post('/items/create/user', json={'email': EMAIL, 'password': PASSWORD})
    data = response.json()
    
    assert response.status_code != 400, "user already exists, but should not"
    assert response.status_code == 200, "response was not 200"
    assert uuid.UUID(data['id']), "ID is not valid"
    assert data['email'] == EMAIL, "email is not the same as the sent one"
    assert 'password' not in data, "password was returned"
    assert data['email_verified'] == False, "email verified before verification email was sent"
    assert data['has_noter_access'] == False, "has noter access before payment"

def test_create_note_unauthenticated():
    response = client.post('/items/create/note', json={'name': 'Unauthenticated', 'path': []})
    assert response.status_code == 401, "response was not 401"

@pre_authenticate
def test_create_note_in_nonexistent_path():
    response = client.post('/items/create/note', json={'name': 'Nonexistent', 'path': ['------------nonexistent------------']})
    assert response.status_code == 400, "response was not 400"

@pre_authenticate
def test_create_note_in_root_path():
    response = client.post('/items/create/note', json={'name': 'Root', 'path': []})
    assert response.status_code == 201, "response was not 201"

@pre_authenticate
def test_create_folder():
    response = client.post('/items/create/folder', json={'name': 'Root Folder', 'path': []})
    data = response.json()

    assert response.status_code == 201, "response was not 201"
    assert uuid.UUID(data['id']), "ID is not valid"
