from sqlalchemy.orm import Session
from app.models.addreses import Addresses
from app.schemas.addresses import AddressCreate
from typing import List


class AddressesRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_addresses(self) -> List[Addresses]:
        """Получить все адреса из базы данных"""
        return self.db.query(Addresses).all()
    
    def get_address_by_id(self, address_id: int) -> Addresses:
        """Получить адрес по ID"""
        return self.db.query(Addresses).filter(Addresses.id == address_id).first()
    
    def create_address(self, address: AddressCreate) -> Addresses:
        """Создать новый адрес"""
        db_address = Addresses(
            number=address.number,
            id_work_shop=address.id_work_shop
        )
        self.db.add(db_address)
        self.db.commit()
        self.db.refresh(db_address)
        return db_address