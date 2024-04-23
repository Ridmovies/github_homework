from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_recipe_by_id():
    response = client.get("/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "cooking_time" in data
    assert "ingredients" in data
    assert "description" in data


def test_get_recipe_by_invalid_id():
    response = client.get("/recipes/999")
    print(response.status_code)
    assert response.status_code == 404
