from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_get_index():
    response = client.get(url="/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_post_index():
    response = client.post(url="/")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
