import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.work_shop import WorkShopRepository
from app.models.work_shops import WorkShop

client = TestClient(app)

class TestCreateWorkShopEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.work_shop.get_db')
    def test_create_work_shop(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект СТО
        mock_work_shop = WorkShop(
            id=1,
            work_shop_name="Тестовое СТО",
            telephone="+7(999)123-45-67",
            street_name="Тестовая улица",
            address="123",
            site="https://test-workshop.ru",
            rating=4.5
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.work_shop.WorkShopRepository', return_value=mock_repo):
            mock_repo.create_work_shop.return_value = mock_work_shop
            
            # Подготавливаем данные для запроса
            work_shop_data = {
                "work_shop_name": "Тестовое СТО",
                "telephone": "+7(999)123-45-67",
                "street_name": "Тестовая улица",
                "address": "123",
                "site": "https://test-workshop.ru",
                "rating": 4.5
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/work_shop/", json=work_shop_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["work_shop_name"], "Тестовое СТО")
            self.assertEqual(data["telephone"], "+7(999)123-45-67")
            self.assertEqual(data["street_name"], "Тестовая улица")
            self.assertEqual(data["address"], "123")
            self.assertEqual(data["site"], "https://test-workshop.ru")
            self.assertEqual(data["rating"], 4.5)

    @patch('app.api.v1.work_shop.get_db')
    def test_create_work_shop_partial_data(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект СТО с частичными данными
        mock_work_shop = WorkShop(
            id=2,
            work_shop_name="Частичное СТО",
            telephone="+7(999)765-43-21",
            street_name=None,
            address=None,
            site=None,
            rating=None
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.work_shop.WorkShopRepository', return_value=mock_repo):
            mock_repo.create_work_shop.return_value = mock_work_shop
            
            # Подготавливаем данные для запроса
            work_shop_data = {
                "work_shop_name": "Частичное СТО",
                "telephone": "+7(999)765-43-21"
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/work_shop/", json=work_shop_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 2)
            self.assertEqual(data["work_shop_name"], "Частичное СТО")
            self.assertEqual(data["telephone"], "+7(999)765-43-21")
            self.assertIsNone(data["street_name"])
            self.assertIsNone(data["address"])
            self.assertIsNone(data["site"])
            self.assertIsNone(data["rating"])

if __name__ == "__main__":
    unittest.main()