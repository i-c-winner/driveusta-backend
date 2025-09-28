from sqlalchemy.orm import Session
from app.models.addreses import Addresses
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