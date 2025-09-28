from sqlalchemy.orm import Session
from app.models.avialableCars import AvialableCars
from typing import List


class AvailableCarsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_available_cars(self) -> List[AvialableCars]:
        """Получить все доступные автомобили из базы данных"""
        return self.db.query(AvialableCars).all()
    
    def get_available_car_by_id(self, available_car_id: int) -> AvialableCars:
        """Получить доступный автомобиль по ID"""
        return self.db.query(AvialableCars).filter(AvialableCars.id == available_car_id).first()