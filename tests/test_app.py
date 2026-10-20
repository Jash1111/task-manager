from app import app, tasks


def setup_function():
    tasks.clear()


def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_home_page_loads():
    r = app.test_client().get("/")
    assert r.status_code == 200
    assert b"Task Manager" in r.data


def test_add_and_delete_task():
    client = app.test_client()
    client.post("/add", data={"title": "Finish CCA 2"})
    assert b"Finish CCA 2" in client.get("/").data
    client.get("/delete/1")
    assert b"Finish CCA 2" not in client.get("/").data
