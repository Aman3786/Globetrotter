from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_game_flow():
    # Test getting a question
    response = client.get("/api/game")
    assert response.status_code == 200
    assert "clues" in response.json()
    assert "options" in response.json()
    
    # Test answer verification
    destination_id = response.json()["destination_id"]
    answer = response.json()["options"][0]
    verify_response = client.post(
        f"/api/verify/{destination_id}",
        json={"answer": answer, "user_id": None}
    )
    
    assert verify_response.status_code == 200
    assert "correct" in verify_response.json()
