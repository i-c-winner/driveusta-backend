from sqlalchemy.orm import Session
from app.models.typeWorkChildren import TypeWorkChildren
from typing import List


class TypeWorkChildrenRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_type_work_children(self) -> List[TypeWorkChildren]:
        """Получить все типы работ детей из базы данных"""
        return self.db.query(TypeWorkChildren).all()
    
    def get_type_work_child_by_id(self, type_work_child_id: int) -> TypeWorkChildren:
        """Получить тип работы ребенка по ID"""
        return self.db.query(TypeWorkChildren).filter(TypeWorkChildren.id == type_work_child_id).first()