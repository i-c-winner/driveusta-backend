from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Photos(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    url= Column(String, nullable=True)
    id_sto = Column(Integer, ForeignKey("sto.id"))

    sto=relationship('Sto', backref='photos')