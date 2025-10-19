from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Numeric, MetaData, Table, ForeignKey, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from starlette import status
from app.services.security.auth.token import create_tokens, create_hash_password

from app.db.dependencies import get_db
from app.models import WorkShop
from app.models.auth import Tokens
from app.schemas.auth import ResponseCreateToken
from app.db.repositories.auth.token import TokenRepository
from app.db.session import engine

router = APIRouter(
    prefix="/register",
    tags=["register"]
)


@router.post(path="/", response_model=ResponseCreateToken)
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    work_shop = db.query(WorkShop).filter(
        WorkShop.username == form_data.username,
    ).first()
    print(work_shop)
    if work_shop:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Такой пользователь существует"
        )
    else:
        result = create_tokens({"work_shop_username": form_data.username})
        print('PSWWORD', form_data.password)
        new_work_shop = WorkShop(
            username=form_data.username,
            hash_password=create_hash_password(form_data.password),
            work_shop_name='',
            telephone='',
            street_name='',
            address='',
            site='',
            rating=0.0)
        tokens = Tokens(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            work_shop_username=form_data.username
        )
        db.add(tokens)
        db.add(new_work_shop)
        db.commit()
        db.refresh(new_work_shop)
        
        # Создаем новую таблицу в схеме prices с именем пользователя
        try:
            # Создаем схему prices, если она не существует
            with engine.connect() as conn:
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS prices"))
                conn.commit()
            
            # Создаем таблицу с именем пользователя в схеме prices
            # Используем текстовый SQL для правильного создания внешнего ключа
            with engine.connect() as conn:
                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS prices."{form_data.username}" (
                    work_type_children_id INTEGER,
                    price NUMERIC(15,0),
                    PRIMARY KEY (work_type_children_id),
                    CONSTRAINT fk_work_type_children 
                        FOREIGN KEY (work_type_children_id) 
                        REFERENCES cars.type_work_children(id)
                        ON DELETE CASCADE
                )
                """
                conn.execute(text(create_table_sql))
                conn.commit()
        except SQLAlchemyError as e:
            # Откатываем транзакцию в случае ошибки создания таблицы
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании таблицы цен: {str(e)}"
            )
        
        print(result)
        return result


@router.post(path='/login', response_model=ResponseCreateToken)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    tokens = db.query(Tokens).filter(Tokens.work_shop_username == form_data.username).first()
    print(tokens, 'TOKENS')
    if tokens:
        return tokens
    else:
        return ResponseCreateToken(access_token='', refresh_token='', work_shop_username='')