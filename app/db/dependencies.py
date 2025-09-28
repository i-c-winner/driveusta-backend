from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def get_db() -> Session:
    """Dependency для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
