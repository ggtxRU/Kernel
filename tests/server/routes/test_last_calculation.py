from starlette.testclient import TestClient


def test_last_calculation(client: TestClient):
    response = client.get('/calculations/last')
    assert response.status_code == 200

