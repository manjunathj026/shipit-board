import pytest

import config
from app import MAX_NOTE_LENGTH, app, notes


@pytest.fixture
def client():
    app.config["TESTING"] = True
    notes.clear()  # start every test with an empty list
    with app.test_client() as test_client:
        yield test_client


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_home_page_shows_banner_message(client):
    response = client.get("/")
    assert response.status_code == 200
    assert config.MESSAGE in response.get_data(as_text=True)


def test_adding_a_note_shows_it_on_the_page(client):
    client.post("/notes", data={"text": "Shipped v1"})
    assert "Shipped v1" in client.get("/").get_data(as_text=True)


def test_blank_note_is_ignored(client):
    client.post("/notes", data={"text": "   "})
    assert notes == []


def test_long_note_is_trimmed(client):
    client.post("/notes", data={"text": "x" * 500})
    assert len(notes[0]) == MAX_NOTE_LENGTH


def test_info_api_has_version_and_commit(client):
    data = client.get("/api/info").get_json()
    assert "version" in data and "commit" in data
