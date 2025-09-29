import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.streets import StreetsRepository
from app.models.streets import Streets

client = TestClient(app)

class TestCreateStreetEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.streets.get_db')
    def test_create_street(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект улицы
        mock_street = Streets(
            id=1,
            street_name="Main Street",
            id_sto=1
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.streets.StreetsRepository', return_value=mock_repo):
            mock_repo.create_street.return_value = mock_street
            
            # Подготавливаем данные для запроса
            street_data = {
                "street_name": "Main Street",
                "id_sto": 1
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/streets/", json=street_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["street_name"], "Main Street")
            self.assertEqual(data["id_sto"], 1)

if __name__ == "__main__":
    unittest.main()