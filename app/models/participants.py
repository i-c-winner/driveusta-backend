from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


class Participants(Base):
    __tablename__ = "participants"
    __table_args__ = {"schema": "participants"}
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    login = Column(String, nullable=True)
    vin = Column(Numeric, nullable=True)
    car_is=Column(String, nullable=True)


    # ПРАВИЛЬНО: car_id как внешний ключ (уберите unique=True)
    car_id = Column(Integer, ForeignKey('cars.cars.id'), nullable=True)

    # Связь с Cars
    car = relationship('Cars', back_populates='participants')