from sqlalchemy.orm import Session
from app.models.cars import Cars
from typing import List


class CarsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_cars(self) -> List[Cars]:
        """Получить все машины из базы данных"""
        return self.db.query(Cars).all()
    
    def get_cars_by_name(self, car_name: str) -> List[Cars]:
        """Получить машины по имени"""
        return self.db.query(Cars).filter(Cars.car_name.ilike(f"%{car_name}%")).all()
    
    def get_car_by_id(self, car_id: int) -> Cars:
        """Получить машину по ID"""
        return self.db.query(Cars).filter(Cars.id == car_id).first()
