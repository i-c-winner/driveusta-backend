from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Holiday(Base):
    __tablename__ = "holidays"

    id=Column(Integer, primary_key=True, index=True)
    work_shop_id=Column(Integer, ForeignKey("work_shop.id"))
    holiday_date=Column(Date, nullable=True)
    description=Column(String(200), nullable=False)

    work_shop=relationship('work_shop', backref='holidays')