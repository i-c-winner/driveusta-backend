from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date
from sqlalchemy.orm import relationship

from app.db.base import Base

class Appointments(Base):
    __tablename__ = "appointments"
    __table_args__ = {"schema": "participants"}

    id=Column(Integer, primary_key=True, index=True)
    client_name=Column(String(100), nullable=True)
    client_phone=Column(String(20), nullable=True)
    car_license_plate=Column(String(10), nullable=True)
    appointment_date=Column(Date, nullable=True)
    appointment_time=Column(Time, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    time = Column(DateTime, nullable=True)
    description=Column(String(200), nullable=False)

    work_type=relationship('TypeWorkChildren',secondary="participants.appointments_work_type_children",  back_populates='appointments')
    work_shop=relationship('work_shop', secondary="participants.appointments_work_shop", backref="appointments")
    cars=relationship('Cars', secondary="participants.appointments_cars", backref="appointments")