from sqlalchemy.orm import Session
from app.models.typeWorkParents import TypeWorkParents
from typing import List


class TypeWorkParentsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_type_work_parents(self) -> List[TypeWorkParents]:
        """Получить все типы работ родителей из базы данных"""
        return self.db.query(TypeWorkParents).all()
    
    def get_type_work_parent_by_id(self, type_work_parent_id: int) -> TypeWorkParents:
        """Получить тип работы родителя по ID"""
        return self.db.query(TypeWorkParents).filter(TypeWorkParents.id == type_work_parent_id).first()