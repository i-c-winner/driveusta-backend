from sqlalchemy.orm import Session
from app.models.work_shops import WorkShop
from app.schemas.work_shop import WorkShopCreate
from typing import List
from pwdlib import PasswordHash


class WorkShopRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_work_shops(self) -> List[WorkShop]:
        """Получить все СТО из базы данных"""
        return self.db.query(WorkShop).all()
    
    def get_work_shop_by_username(self, work_shop_username: str) -> WorkShop:
        """Получить СТО по ID"""
        return self.db.query(WorkShop).filter(WorkShop.username == work_shop_username).first()
    def get_current_work_shop(self, username):
        return self.db.query(WorkShop).filter(WorkShop.username == username).first()
    def verification_password(self,username,  password):
        password_hash = PasswordHash
        username = self.db.query(WorkShop).filter(WorkShop.username == username).first()
        if not username:
            return False
        return password_hash.verify(password, username.hash_password)

    def get_work_shop_by_address(self, street_name: str, address: str) -> List[WorkShop]:
        """Получить СТО по названию улицы и адресу"""
        return self.db.query(WorkShop).filter(WorkShop.street_name == street_name, WorkShop.address == address).all()
    def get_work_shop(self, login):
        return self.db.query(WorkShop).filter(WorkShop.login == login).first()
    def create_work_shop(self, work_shop: WorkShopCreate) -> WorkShop:
        """Создать новое СТО"""
        db_work_shop = WorkShop(
            work_shop_name='',
            telephone='',
            street_name='',
            address='',
            site='',
            rating='',
            username=work_shop.username,
            hash_password=work_shop.hash_password
        )
        self.db.add(db_work_shop)
        self.db.commit()
        self.db.refresh(db_work_shop)
        return db_work_shop

    def update_work_shop(self, work_shop_id: int, work_shop_data: WorkShopCreate) -> WorkShop:
        """Обновить данные СТО"""
        db_work_shop = self.get_work_shop_by_id(work_shop_id)
        if not db_work_shop:
            return None  # или можно выбросить исключение
        else:
          # Обновляем поля
          db_work_shop.work_shop_name = work_shop_data.work_shop_name
          db_work_shop.telephone = work_shop_data.telephone
          db_work_shop.street_name = work_shop_data.street_name
          db_work_shop.address = work_shop_data.address
          db_work_shop.site = work_shop_data.site
          db_work_shop.rating = work_shop_data.rating
          db_work_shop.hash_password = work_shop_data.hash_password

        self.db.commit()
        self.db.refresh(db_work_shop)
        return db_work_shop
