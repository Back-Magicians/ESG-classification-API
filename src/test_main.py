from fastapi.testclient import TestClient
from main import app
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

def test_root_endpoint():
    """Тестирование корневой конечной точки (/) для проверки корректного возврата HTML содержимого."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<!DOCTYPE html>" in response.text

def test_root_endpoint_not_found():
    """Тестирование корневой конечной точки (/) для проверки корректной обработки отсутствия index.html."""
    original_views_path = app.VIEWS_PATH  # Сохранение оригинального пути
    app.VIEWS_PATH = "./nonexistent_views"  # Временное изменение на несуществующий путь
    response = client.get("/")
    assert response.status_code == 404
    app.VIEWS_PATH = original_views_path  # Восстановление оригинального пути

def test_predict_endpoint():
    """Тестирование конечной точки предсказаний (/predict/) для проверки корректной обработки текста."""
    sample_text = "Это пример текста для классификации ESG рисков."
    response = client.post("/predict/", json={"text": sample_text})
    assert response.status_code == 200
    assert "result" in response.json()  #

def test_predict_endpoint_validation():
    """Тестирование конечной точки предсказаний (/predict/) для проверки корректной обработки некорректного ввода."""
    response = client.post("/predict/", json={})
    assert response.status_code == 422  # Статус код для ошибок валидации