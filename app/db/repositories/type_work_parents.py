from sqlalchemy.orm import Session
from app.models.type_work_parents import TypeWorkParents
from app.schemas.type_work_parents import TypeWorkParentCreate
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
    
    def create_type_work_parent(self, type_work_parent: TypeWorkParentCreate) -> TypeWorkParents:
        """Создать новый тип работы родителя"""
        db_type_work_parent = TypeWorkParents(
            type_work_parent_name=type_work_parent.type_work_parent_name
        )
        self.db.add(db_type_work_parent)
        self.db.commit()
        self.db.refresh(db_type_work_parent)
        return db_type_work_parent