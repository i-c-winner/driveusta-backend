from sqlalchemy.orm import Session
from app.models.streets import Streets
from app.schemas.streets import StreetCreate
from typing import List


class StreetsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_streets(self) -> List[Streets]:
        """Получить все улицы из базы данных"""
        return self.db.query(Streets).all()
    
    def get_street_by_id(self, street_id: int) -> Streets:
        """Получить улицу по ID"""
        return self.db.query(Streets).filter(Streets.id == street_id).first()
    
    def create_street(self, street: StreetCreate) -> Streets:
        """Создать новую улицу"""
        db_street = Streets(
            street_name=street.street_name,
            id_work_shop=street.id_work_shop
        )
        self.db.add(db_street)
        self.db.commit()
        self.db.refresh(db_street)
        return db_street