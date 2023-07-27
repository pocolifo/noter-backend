from .context import client, TEST_USER_EMAIL, TEST_USER_PASSWORD

def test_authentication():
    response = client.post('/authenticate', json={'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})

    assert response.status_code == 200, "response was not a 200"
    assert response.json()['authenticated'] == True, "did not authenticate with correct credentials"