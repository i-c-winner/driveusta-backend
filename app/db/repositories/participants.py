from sqlalchemy.orm import Session
from app.models.participants import Participants
from app.schemas.participants import ParticipantCreate
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
    
    def create_participant(self, participant: ParticipantCreate) -> Participants:
        """Создать нового участника"""
        db_participant = Participants(
            name=participant.name,
            password=participant.password,
            login=participant.login,
            vin=participant.vin,
            car_id=participant.car_id
        )
        self.db.add(db_participant)
        self.db.commit()
        self.db.refresh(db_participant)
        return db_participant