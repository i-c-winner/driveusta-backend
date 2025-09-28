from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


class Participants(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    login = Column(String, nullable=True)
    vin = Column(Numeric, nullable=True)

    # ПРАВИЛЬНО: car_id как внешний ключ (уберите unique=True)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=True)

    # Связь с Cars
    car = relationship('Cars', back_populates='participants')