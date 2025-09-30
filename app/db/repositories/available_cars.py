from sqlalchemy.orm import Session
from app.models.avialableCars import AvialableCars
from app.schemas.available_cars import AvailableCarCreate
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
    
    def create_available_car(self, available_car: AvailableCarCreate) -> AvialableCars:
        """Создать новый доступный автомобиль"""
        db_available_car = AvialableCars(
            car_name=available_car.car_name,
            work_shop_id=available_car.work_shop_id,
            cars_id=available_car.cars_id
        )
        self.db.add(db_available_car)
        self.db.commit()
        self.db.refresh(db_available_car)
        return db_available_car