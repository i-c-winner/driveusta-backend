from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Addresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=True)
    id_sto = Column(Integer, ForeignKey("sto.id"))

    sto= relationship('Sto', backref='addresses')