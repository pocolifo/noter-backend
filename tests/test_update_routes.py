from .conftest import pre_authenticate
from .context import client

@pre_authenticate
def test_update_metadata_note_name():
    create_note_response = client.post('/items/create/note', json={'name': 'test_update_metadata_note_name Note', 'path': []})
    note_id = create_note_response.json()['id']

    response = client.post('/items/update/metadata', params={'id': note_id}, json={'name': 'test_update_metadata_note_name Note (updated)', 'path': []})
    assert response.status_code == 204

    get_note_response = client.get(f'/items/{note_id}')
    assert get_note_response.json()['name'] == 'test_update_metadata_note_name Note (updated)'
