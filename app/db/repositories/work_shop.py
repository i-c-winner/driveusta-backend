from sqlalchemy.orm import Session
from app.models.work_shops import WorkShop
from typing import List


class WorkShopRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_work_shops(self) -> List[WorkShop]:
        """Получить все СТО из базы данных"""
        return self.db.query(WorkShop).all()
    
    def get_work_shop_by_id(self, work_shop_id: int) -> WorkShop:
        """Получить СТО по ID"""
        return self.db.query(WorkShop).filter(WorkShop.id == work_shop_id).first()

    def get_work_shop_by_address(self, street_name: str, address: str) -> List[WorkShop]:
        """Получить СТО по названию улицы и адресу"""
        return self.db.query(WorkShop).filter(WorkShop.street_name == street_name, WorkShop.address == address).all()