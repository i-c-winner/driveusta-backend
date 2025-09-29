import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.repositories.type_work_children import TypeWorkChildrenRepository
from app.models.typeWorkChildren import TypeWorkChildren

client = TestClient(app)

class TestCreateTypeWorkChildEndpoint(unittest.TestCase):
    
    @patch('app.api.v1.type_work_children.get_db')
    def test_create_type_work_child(self, mock_get_db):
        # Создаем моковые данные
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Создаем моковый объект типа работы ребенка
        mock_type_work_child = TypeWorkChildren(
            id=1,
            type_work_child_name="Engine Repair",
            parent_id=1
        )
        
        # Настраиваем мок репозитория
        mock_repo = MagicMock()
        with patch('app.api.v1.type_work_children.TypeWorkChildrenRepository', return_value=mock_repo):
            mock_repo.create_type_work_child.return_value = mock_type_work_child
            
            # Подготавливаем данные для запроса
            type_work_child_data = {
                "type_work_child_name": "Engine Repair",
                "parent_id": 1
            }
            
            # Выполняем POST запрос
            response = client.post("/api/v1/type-work-children/", json=type_work_child_data)
            
            # Проверяем результат
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], 1)
            self.assertEqual(data["type_work_child_name"], "Engine Repair")
            self.assertEqual(data["parent_id"], 1)

if __name__ == "__main__":
    unittest.main()