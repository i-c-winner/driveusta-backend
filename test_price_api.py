from fastapi.testclient import TestClient
from app.main import app

def test_price_api():
    """
    Пример использования API для цен
    """
    # Создаем тестовый клиент
    client = TestClient(app)
    
    # Сначала регистрируем пользователя, чтобы создать таблицу цен
    register_response = client.post(
        "/api/v1/register/",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    print(f"Register response status: {register_response.status_code}")
    
    # Теперь создаем запись цены
    price_data = {
        "username": "testuser",
        "work_type_children_id": 1,
        "price": 1500.0
    }
    
    response = client.post("/api/v1/price/", json=price_data)
    
    print(f"Create price response status: {response.status_code}")
    print(f"Create price response data: {response.json()}")
    
    # Проверяем, что можем получить запись
    get_response = client.get("/api/v1/price/testuser/1")
    print(f"Get price response status: {get_response.status_code}")
    print(f"Get price response data: {get_response.json()}")


if __name__ == "__main__":
    test_price_api()