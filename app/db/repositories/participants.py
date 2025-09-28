from sqlalchemy.orm import Session
from app.models.participants import Participants
from typing import List


class ParticipantsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_participants(self) -> List[Participants]:
        """Получить всех участников из базы данных"""
        return self.db.query(Participants).all()
    
    def get_participant_by_id(self, participant_id: int) -> Participants:
        """Получить участника по ID"""
        return self.db.query(Participants).filter(Participants.id == participant_id).first()