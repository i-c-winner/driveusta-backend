from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db.repositories.price import PriceRepository
from app.schemas.price import PriceCreate, PriceResponse
from app.services.security.auth.token import get_current_username

router = APIRouter(
    prefix="/price",
    tags=["price"]
)


@router.post("/", response_model=PriceResponse)
async def create_price_record(
    price_data: PriceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_username)
):
    """
    Создает или обновляет запись цены в таблице пользователя в схеме prices
    
    Parameters:
    - work_type_children_id: ID типа работы
    - price: цена
    
    Returns:
    - PriceResponse: созданная/обновленная запись цены
    """
    # Используем имя текущего пользователя для таблицы цен
    username = current_user["username"]
        
    price_repo = PriceRepository(db)
    try:
        result = price_repo.create_price_record(
            username=username,
            work_type_children_id=price_data.work_type_children_id,
            price=price_data.price
        )
        return result
    except Exception as e:
        raise e


@router.get("/{work_type_children_id}", response_model=PriceResponse)
async def get_price_record(
    work_type_children_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_username)
):
    """
    Получает запись цены по типу работы для текущего пользователя
    
    Parameters:
    - work_type_children_id: ID типа работы
    
    Returns:
    - PriceResponse: запись цены или null, если не найдена
    """
    price_repo = PriceRepository(db)
    try:
        result = price_repo.get_price_by_work_type(
            username=current_user["username"],
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