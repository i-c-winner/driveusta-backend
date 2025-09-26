from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base

class Participants(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    password= Column(String, nullable=True)
    login = Column(String, nullable=True)
    vin = Column(Numeric, nullable=True)
    car_id = Column(Integer, ForeignKey("cars.id"))

    car=relationship('Cars', backref='participants')