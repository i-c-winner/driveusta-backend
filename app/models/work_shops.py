from sqlalchemy import Column, Integer, String, Numeric, Float
from sqlalchemy.orm import relationship
from app.db.base import Base


class WorkShop(Base):
    __tablename__ = "work_shop"
    __table_args__ = {"schema": "work_shop"}

    id = Column(Integer, primary_key=True, index=True)
    work_shop_name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    street_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    site = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    hash_password = Column(String, nullable=False, server_default='')
    username = Column(String, nullable=False, server_default='')
    
    holidays = relationship('Holidays', secondary='work_shop.holidays_work_shops', back_populates='work_shop')