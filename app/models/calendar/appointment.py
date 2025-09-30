from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date
from sqlalchemy.orm import relationship

from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id=Column(Integer, primary_key=True, index=True)
    work_shop_id=Column(Integer, ForeignKey("work_shop.id"))
    client_name=Column(String(100), nullable=True)
    client_phone=Column(String(20), nullable=True)
    cars_id=Column(Integer, ForeignKey("cars.id"))
    car_license_plate=Column(String(10), nullable=True)
    work_type=Column(Integer, ForeignKey("type_work_children.id"))
    appointment_date=Column(Date, nullable=True)
    appointment_time=Column(Time, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    time = Column(DateTime, nullable=True)
    description=Column(String(200), nullable=False)

    work_shop= relationship('work_shop', backref='appointments')
    car=relationship('Cars', backref='appointments')
    type_work=relationship('type_work_children', backref='appointments')