from fastapi.testclient import TestClient
import time
from main import app

client = TestClient(app)


def test_create_task():
    response = client.post("/task", json={"duration": 1})
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

    time.sleep(3)

    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    # assert response.json() == {"status": "done"}
