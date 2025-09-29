import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.photos import PhotosRepository
from app.models.photos import Photos

client = TestClient(app)

class TestCreatePhotoEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.photos.get_db')
    def test_create_photo(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект фотографии
        mock_photo = Photos(
            id=1,
            url="http://example.com/photo.jpg",
            id_sto=1
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.photos.PhotosRepository', return_value=mock_repo):
            mock_repo.create_photo.return_value = mock_photo
            
            # Подготавливаем данные для запроса
            photo_data = {
                "url": "http://example.com/photo.jpg",
                "id_sto": 1
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/photos/", json=photo_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["url"], "http://example.com/photo.jpg")
            self.assertEqual(data["id_sto"], 1)

if __name__ == "__main__":
    unittest.main()