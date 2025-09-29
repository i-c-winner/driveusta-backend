from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.participants import ParticipantsRepository
from app.schemas.participants import ParticipantResponse, ParticipantsListResponse, ParticipantCreate

router = APIRouter(
    prefix="/participants",
    tags=["participants"]
)

@router.post("/", response_model=ParticipantResponse)
async def create_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    """
    Создать нового участника
    """
    try:
        participants_repo = ParticipantsRepository(db)
        new_participant = participants_repo.create_participant(participant)
        
        participant_response = ParticipantResponse.model_validate(new_participant)
        return participant_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании записи: {str(e)}")

@router.get("/", response_model=ParticipantsListResponse)
async def get_participants(db: Session = Depends(get_db)):
    """
    Получить список всех участников из базы данных
    """
    try:
        participants_repo = ParticipantsRepository(db)
        participants = participants_repo.get_all_participants()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        participant_responses = [ParticipantResponse.model_validate(participant) for participant in participants]
        
        return ParticipantsListResponse(participants=participant_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{participant_id}", response_model=ParticipantResponse)
async def get_participant_by_id(participant_id: int, db: Session = Depends(get_db)):
    """
    Получить участника по ID
    """
    try:
        participants_repo = ParticipantsRepository(db)
        participant = participants_repo.get_participant_by_id(participant_id)
        
        if participant is None:
            raise HTTPException(status_code=404, detail=f"Участник с ID {participant_id} не найден")
        
        participant_response = ParticipantResponse.model_validate(participant)
        return participant_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")