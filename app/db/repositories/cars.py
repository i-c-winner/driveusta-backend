from sqlalchemy.orm import Session
from app.models.cars import Cars
from app.schemas.cars import CarCreate
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
    
    def create_car(self, car: CarCreate) -> Cars:
        """Создать новую машину"""
        db_car = Cars(
            car_name=car.car_name,
            brand=car.brand,
            model=car.model,
            year=car.year
        )
        self.db.add(db_car)
        self.db.commit()
        self.db.refresh(db_car)
        return db_car