from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FinTrack API. Visit /docs for the API documentation."}

def test_get_transactions_empty():
    response = client.get("/transactions/")
    assert response.status_code == 200
    # Before adding any data, should be empty list
    assert response.json() == []

def test_get_summary_empty():
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    assert response.json() == {
        "total_income": 0.0,
        "total_expenses": 0.0,
        "net_savings": 0.0
    }
