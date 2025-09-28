from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class AvialableCars(Base):
    __tablename__ = "avialable_cars"
    id = Column(Integer, primary_key=True, index=True)
    car_name = Column(String, nullable=True)
    sto_id = Column(Integer, ForeignKey("sto.id"))
    cars_id = Column(Integer, ForeignKey("cars.id"))  # Добавляем внешний ключ

    sto = relationship('Sto', backref='sto')
    cars = relationship('Cars', backref='avialable_cars')