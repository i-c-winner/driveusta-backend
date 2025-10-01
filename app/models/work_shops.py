from sqlalchemy import Column, Integer, String, Numeric, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class work_shop(Base):
    __tablename__ = "work_shop"
    __table_args__ = {"schema": "work_shop"}

    id = Column(Integer, primary_key=True, index=True)
    work_shop_name = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    street_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    site = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    
    holidays = relationship('Holidays', secondary='work_shop.holidays_work_shops', back_populates='work_shop')