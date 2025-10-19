from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db.repositories.price import PriceRepository
from app.schemas.price import PriceCreate, PriceResponse

router = APIRouter(
    prefix="/price",
    tags=["price"]
)


@router.post("/", response_model=PriceResponse)
async def create_price_record(
    price_data: PriceCreate,
    db: Session = Depends(get_db)
):
    """
    Создает или обновляет запись цены в таблице пользователя в схеме prices
    
    Parameters:
    - username: имя пользователя (используется как имя таблицы)
    - work_type_children_id: ID типа работы
    - price: цена
    
    Returns:
    - PriceResponse: созданная/обновленная запись цены
    """
    price_repo = PriceRepository(db)
    try:
        result = price_repo.create_price_record(
            username=price_data.username,
            work_type_children_id=price_data.work_type_children_id,
            price=price_data.price
        )
        return result
    except Exception as e:
        raise e


@router.get("/{username}/{work_type_children_id}", response_model=PriceResponse)
async def get_price_record(
    username: str,
    work_type_children_id: int,
    db: Session = Depends(get_db)
):
    """
    Получает запись цены по типу работы для пользователя
    
    Parameters:
    - username: имя пользователя (используется как имя таблицы)
    - work_type_children_id: ID типа работы
    
    Returns:
    - PriceResponse: запись цены или null, если не найдена
    """
    price_repo = PriceRepository(db)
    try:
        result = price_repo.get_price_by_work_type(
            username=username,
            work_type_children_id=work_type_children_id
        )
        
        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Запись цены не найдена"
            )
            
        return result
    except Exception as e:
        raise e