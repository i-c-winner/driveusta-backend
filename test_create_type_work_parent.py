import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.type_work_parents import TypeWorkParentsRepository
from app.models.type_work_parents import TypeWorkParents

client = TestClient(app)

class TestCreateTypeWorkParentEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.type_work_parents.get_db')
    def test_create_type_work_parent(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект типа работы родителя
        mock_type_work_parent = TypeWorkParents(
            id=1,
            type_work_parent_name="Major Repair"
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.type_work_parents.TypeWorkParentsRepository', return_value=mock_repo):
            mock_repo.create_type_work_parent.return_value = mock_type_work_parent
            
            # Подготавливаем данные для запроса
            type_work_parent_data = {
                "type_work_parent_name": "Major Repair"
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/type-work-parents/", json=type_work_parent_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["type_work_parent_name"], "Major Repair")

if __name__ == "__main__":
    unittest.main()