from sqlalchemy.orm import Session
from app.models.photos import Photos
from app.schemas.photos import PhotoCreate
from typing import List


class PhotosRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_photos(self) -> List[Photos]:
        """Получить все фотографии из базы данных"""
        return self.db.query(Photos).all()
    
    def get_photo_by_id(self, photo_id: int) -> Photos:
        """Получить фотографию по ID"""
        return self.db.query(Photos).filter(Photos.id == photo_id).first()
    
    def create_photo(self, photo: PhotoCreate) -> Photos:
        """Создать новую фотографию"""
        db_photo = Photos(
            url=photo.url,
            id_work_shop=photo.id_work_shop
        )
        self.db.add(db_photo)
        self.db.commit()
        self.db.refresh(db_photo)
        return db_photo