from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tokens(Base):
    __tablename__ = "token"

    access_token= Column(String, primary_key=True, nullable=False)
    refresh_token= Column(String, nullable=False)
    work_shop_username = Column(String, ForeignKey("work_shop.work_shop.username"), nullable=False)

    work_shop= relationship('WorkShop', backref='auth')