from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Photos(Base):
    __tablename__ = "photos"
    __table_args__ = {"schema": "work_shop"}
    
    id = Column(Integer, primary_key=True, index=True)
    url= Column(String, nullable=True)
    id_work_shop = Column(Integer, ForeignKey("work_shop.work_shop.id"))

    work_shop=relationship('WorkShop', backref='photos')