from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_expense():
    response = client.post(
        "/expenses",
        json={
            "title": "Test coffee",
            "category": "Food",
            "amount": 15.5,
            "date": "2026-05-19"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test coffee"
    assert data["category"] == "Food"
    assert data["amount"] == 15.5


def test_get_expenses():
    response = client.get("/expenses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_expense():
    create_response = client.post(
        "/expenses",
        json={
            "title": "Delete me",
            "category": "Test",
            "amount": 10.0,
            "date": "2026-05-19"
        }
    )

    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")

    assert delete_response.status_code == 200