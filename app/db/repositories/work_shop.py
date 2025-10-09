from sqlalchemy.orm import Session
from app.models.work_shops import WorkShop
from app.schemas.work_shop import WorkShopCreate
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
    def get_work_shop(self, login):
        return self.db.query(WorkShop).filter(WorkShop.login == login).first()
    def create_work_shop(self, work_shop: WorkShopCreate) -> WorkShop:
        """Создать новое СТО"""
        db_work_shop = WorkShop(
            work_shop_name=work_shop.work_shop_name,
            telephone=work_shop.telephone,
            street_name=work_shop.street_name,
            address=work_shop.address,
            site=work_shop.site,
            rating=work_shop.rating,
            hash_password=work_shop.hash_password
        )
        self.db.add(db_work_shop)
        self.db.commit()
        self.db.refresh(db_work_shop)
        return db_work_shop