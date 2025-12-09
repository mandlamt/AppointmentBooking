from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app import models
import datetime


client = TestClient(app)


def setup_module(module):
    # recreate database
    models.Base.metadata.drop_all(bind=engine)
    init_db()


def test_create_and_list():
    start = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end = start + datetime.timedelta(hours=1)
    payload = {
        "name": "Bob",
        "email": "bob@example.com",
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "notes": "Initial booking",
    }
    r = client.post("/appointments", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["name"] == "Bob"

    r2 = client.get("/appointments")
    assert r2.status_code == 200
    arr = r2.json()
    assert len(arr) == 1


def test_overlap_rejected():
    # create an appointment
    start = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    end = start + datetime.timedelta(hours=2)
    payload = {
        "name": "Carol",
        "email": "carol@example.com",
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
    }
    r = client.post("/appointments", json=payload)
    assert r.status_code == 200

    # attempt overlapping
    overlap_payload = {
        "name": "Dan",
        "email": "dan@example.com",
        "start_time": (start + datetime.timedelta(hours=1)).isoformat(),
        "end_time": (end + datetime.timedelta(hours=1)).isoformat(),
    }
    r2 = client.post("/appointments", json=overlap_payload)
    assert r2.status_code == 400
