import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.cars import CarsRepository
from app.models.cars import Cars

client = TestClient(app)

class TestCreateCarEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.cars.get_db')
    def test_create_car(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект машины
        mock_car = Cars(
            id=1,
            car_name="Toyota Camry",
            brand="Toyota",
            model="Camry",
            year=2020
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.cars.CarsRepository', return_value=mock_repo):
            mock_repo.create_car.return_value = mock_car
            
            # Подготавливаем данные для запроса
            car_data = {
                "car_name": "Toyota Camry",
                "brand": "Toyota",
                "model": "Camry",
                "year": 2020
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/cars/", json=car_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["car_name"], "Toyota Camry")
            self.assertEqual(data["brand"], "Toyota")
            self.assertEqual(data["model"], "Camry")
            self.assertEqual(data["year"], 2020)

if __name__ == "__main__":
    unittest.main()