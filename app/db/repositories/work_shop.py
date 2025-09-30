from sqlalchemy.orm import Session
from app.models.work_shop import work_shop
from typing import List


class work_shopRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_work_shops(self) -> List[work_shop]:
        """Получить все СТО из базы данных"""
        return self.db.query(work_shop).all()
    
    def get_work_shop_by_id(self, work_shop_id: int) -> work_shop:
        """Получить СТО по ID"""
        return self.db.query(work_shop).filter(work_shop.id == work_shop_id).first()

    def get_work_shop_by_address(self, street_name: str, address: str) -> List[work_shop]:
        """Получить СТО по названию улицы и адресу"""
        return self.db.query(work_shop).filter(work_shop.street_name == street_name, work_shop.address == address).all()