# USE PYTEST
from requests import Session

s = Session()

# auth data for testing so every endpoint wont fail due to lack of authentication
AUTH_EMAIL = ""
AUTH_PASSWORD = ""


def auth(email:str, password:str):
    global s
    r = s.post("http://localhost:8000/authenticate", json={"email":email, "password":password})
    return r.status_code

def update_metadata(id:str, name:str, path:list):
    r = s.post("http://localhost:8000/items/update/metadata?id={0}".format(id), json={"name":name, "path":path})
    return r.status_code

def update_blocks(id:str, blocks:list):
    r = s.put("http://localhost:8000/items/update/blocks?id={0}".format(id), json=blocks)
    return r.status_code

def create_user(email:str, password:str):
    r = s.post("http://localhost:8000/items/create/user", json={"email":email, "password":password})
    return r.status_code
    
def create_note(name:str, path:str):
    r = s.post("http://localhost:8000/items/create/note", json={"name":name, "path":path})
    return r.status_code
    
def create_folder(name:str, path:str):
    r = s.post("http://localhost:8000/items/create/folder", json={"name":name, "path":path})
    return r.status_code
    
def get_item(id:str):
    r = s.get("http://localhost:8000/items/{0}".format(id))
    return r.status_code

def list_notes(path:list):
    r = s.post("http://localhost:8000/items/list", json=path)
    return r.status_code



# TESTS
def test_auth():
    assert auth("", "") == 200 # not using global auth so you can test this endpoint explicitly
    
def test_metadata():
    auth(AUTH_EMAIL, AUTH_PASSWORD)
    assert update_metadata("", "", []) == 204
    
def test_blocks():
    auth(AUTH_EMAIL, AUTH_PASSWORD)
    assert update_blocks("", []) == 204
    
def test_createuser():
    auth(AUTH_EMAIL, AUTH_PASSWORD)
    assert create_user("", "") == 201
    
def test_createnote():
    auth(AUTH_EMAIL, AUTH_PASSWORD)
    assert create_note("", "") == 201
    
def test_createfolder():
    auth(AUTH_EMAIL, AUTH_PASSWORD)
    assert create_folder("", "") == 201
    
def test_getitem():
    auth(AUTH_EMAIL, AUTH_PASSWORD)
    assert get_item("") == 200
    
def test_listitems():
    auth(AUTH_EMAIL, AUTH_PASSWORD)
    assert list_notes([]) == 200


