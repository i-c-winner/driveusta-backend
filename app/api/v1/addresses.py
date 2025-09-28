from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.addresses import AddressesRepository
from app.schemas.addresses import AddressResponse, AddressesListResponse

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"]
)

@router.get("/", response_model=AddressesListResponse)
async def get_addresses(db: Session = Depends(get_db)):
    """
    Получить список всех адресов из базы данных
    """
    try:
        addresses_repo = AddressesRepository(db)
        addresses = addresses_repo.get_all_addresses()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        address_responses = [AddressResponse.model_validate(address) for address in addresses]
        
        return AddressesListResponse(addresses=address_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{address_id}", response_model=AddressResponse)
async def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    """
    Получить адрес по ID
    """
    try:
        addresses_repo = AddressesRepository(db)
        address = addresses_repo.get_address_by_id(address_id)
        
        if address is None:
            raise HTTPException(status_code=404, detail=f"Адрес с ID {address_id} не найден")
        
        address_response = AddressResponse.model_validate(address)
        return address_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")