import pytest
from fastapi.testclient import TestClient
from app import app

test_client = TestClient(app)


@pytest.mark.end_to_end
def test_read_main():
    # TODO: current test requires API connectivity and isn't deterministic
    response = test_client.get("/quote/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['author'] and json_response['quote']
