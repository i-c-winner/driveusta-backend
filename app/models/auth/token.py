from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tokens(Base):
    __tablename__ = "token"

    hash_token= Column(String, primary_key=True, nullable=False)
    token_type= Column(String, nullable=False)
    id_work_shop= Column(Integer, ForeignKey("work_shop.work_shop.id"), nullable=False)

    work_shop= relationship('WorkShop', backref='auth')