from sqlalchemy.orm import Session
from app.models.type_work_children import TypeWorkChildren
from app.schemas.type_work_children import TypeWorkChildCreate
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
    
    def create_type_work_child(self, type_work_child: TypeWorkChildCreate) -> TypeWorkChildren:
        """Создать новый тип работы ребенка"""
        db_type_work_child = TypeWorkChildren(
            type_work_child_name=type_work_child.type_work_child_name,
            parent_id=type_work_child.parent_id
        )
        self.db.add(db_type_work_child)
        self.db.commit()
        self.db.refresh(db_type_work_child)
        return db_type_work_child