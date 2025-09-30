from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class AvialableCars(Base):
    __tablename__ = "avialable_cars"
    id = Column(Integer, primary_key=True, index=True)
    car_name = Column(String, nullable=True)
    work_shop_id = Column(Integer, ForeignKey("work_shop.id"))
    cars_id = Column(Integer, ForeignKey("cars.id"))  # Добавляем внешний ключ

    work_shop = relationship('work_shop', backref='work_shop')
    cars = relationship('Cars', backref='avialable_cars')