from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.photos import PhotosRepository
from app.schemas.photos import PhotoResponse, PhotosListResponse

router = APIRouter(
    prefix="/photos",
    tags=["photos"]
)

@router.get("/", response_model=PhotosListResponse)
async def get_photos(db: Session = Depends(get_db)):
    """
    Получить список всех фотографий из базы данных
    """
    try:
        photos_repo = PhotosRepository(db)
        photos = photos_repo.get_all_photos()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        photo_responses = [PhotoResponse.model_validate(photo) for photo in photos]
        
        return PhotosListResponse(photos=photo_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo_by_id(photo_id: int, db: Session = Depends(get_db)):
    """
    Получить фотографию по ID
    """
    try:
        photos_repo = PhotosRepository(db)
        photo = photos_repo.get_photo_by_id(photo_id)
        
        if photo is None:
            raise HTTPException(status_code=404, detail=f"Фотография с ID {photo_id} не найдена")
        
        photo_response = PhotoResponse.model_validate(photo)
        return photo_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")