from .conftest import pre_authenticate
from .context import client

@pre_authenticate
def test_get_item():
    create_note_response = client.post('/items/create/note', json={'name': 'Get Item Test Note', 'path': []})
    note_id = create_note_response.json()['id']

    response = client.get(f'/items/{note_id}')
    data = response.json()

    assert response.status_code == 200, "expected 200"
    assert data['id'] == note_id, "ID got is not the one requested"
    assert data['name'] == 'Get Item Test Note', "name is not the same as created"
    assert data['path'] == [], "path is not the same as created"

@pre_authenticate
def test_list_items():
    response = client.post("/items/list", json=[])
    data = response.json()

    assert response.status_code == 200, "response was not 200"
    assert type(data) == list, "response is not list"

@pre_authenticate
def test_list_items_nonexistent_path():
    response = client.post("/items/list", json=['------------nonexistent------------'])
    assert response.status_code == 400, "response was not 400"
