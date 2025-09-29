import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.participants import ParticipantsRepository
from app.models.participants import Participants

client = TestClient(app)

class TestCreateParticipantEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.participants.get_db')
    def test_create_participant(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект участника
        mock_participant = Participants(
            id=1,
            name="John Doe",
            password="secret",
            login="johndoe",
            vin=123456789,
            car_id=1
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.participants.ParticipantsRepository', return_value=mock_repo):
            mock_repo.create_participant.return_value = mock_participant
            
            # Подготавливаем данные для запроса
            participant_data = {
                "name": "John Doe",
                "password": "secret",
                "login": "johndoe",
                "vin": 123456789,
                "car_id": 1
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/participants/", json=participant_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["name"], "John Doe")
            self.assertEqual(data["password"], "secret")
            self.assertEqual(data["login"], "johndoe")
            self.assertEqual(data["vin"], 123456789)
            self.assertEqual(data["car_id"], 1)

if __name__ == "__main__":
    unittest.main()