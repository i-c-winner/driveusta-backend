import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.addresses import AddressesRepository
from app.models.addreses import Addresses

client = TestClient(app)

class TestCreateAddressEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.addresses.get_db')
    def test_create_address(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект адреса
        mock_address = Addresses(
            id=1,
            number="123",
            id_work_shop=1
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.addresses.AddressesRepository', return_value=mock_repo):
            mock_repo.create_address.return_value = mock_address
            
            # Подготавливаем данные для запроса
            address_data = {
                "number": "123",
                "id_work_shop": 1
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/addresses/", json=address_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["number"], "123")
            self.assertEqual(data["id_work_shop"], 1)

if __name__ == "__main__":
    unittest.main()