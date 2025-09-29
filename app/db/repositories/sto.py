from sqlalchemy.orm import Session
from app.models.sto import Sto
from typing import List


class StoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_stos(self) -> List[Sto]:
        """Получить все СТО из базы данных"""
        return self.db.query(Sto).all()
    
    def get_sto_by_id(self, sto_id: int) -> Sto:
        """Получить СТО по ID"""
        return self.db.query(Sto).filter(Sto.id == sto_id).first()

    def get_sto_by_address(self, street_name: str, address: str) -> List[Sto]:
        """Получить СТО по названию улицы и адресу"""
        return self.db.query(Sto).filter(Sto.street_name == street_name, Sto.address == address).all()