import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.available_cars import AvailableCarsRepository
from app.models.avialableCars import AvialableCars

client = TestClient(app)

class TestCreateAvailableCarEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.available_cars.get_db')
    def test_create_available_car(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект доступного автомобиля
        mock_available_car = AvialableCars(
            id=1,
            car_name="Toyota Camry",
            sto_id=1,
            cars_id=1
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.available_cars.AvailableCarsRepository', return_value=mock_repo):
            mock_repo.create_available_car.return_value = mock_available_car
            
            # Подготавливаем данные для запроса
            available_car_data = {
                "car_name": "Toyota Camry",
                "sto_id": 1,
                "cars_id": 1
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/available-cars/", json=available_car_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["car_name"], "Toyota Camry")
            self.assertEqual(data["sto_id"], 1)
            self.assertEqual(data["cars_id"], 1)

if __name__ == "__main__":
    unittest.main()