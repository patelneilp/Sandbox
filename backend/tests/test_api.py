import asyncio

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_job_lifecycle_endpoints():
    create = client.post("/analyze", json={"entities": ["aspirin", "CHEMBL25"]})
    assert create.status_code == 200
    job_id = create.json()["jobId"]

    state = "queued"
    for _ in range(30):
        status = client.get(f"/status/{job_id}")
        assert status.status_code == 200
        state = status.json()["state"]
        if state in {"completed", "failed"}:
            break
        asyncio.run(asyncio.sleep(0.05))

    assert state == "completed"
    results = client.get(f"/results/{job_id}")
    assert results.status_code == 200
    body = results.json()
    assert body["job_id"] == job_id
    assert len(body["rankings"]) == 2
