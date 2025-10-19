from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from starlette import status


class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_price_record(self, username: str, work_type_children_id: int, price: float):
        """
        Создает запись цены в таблице пользователя в схеме prices
        """
        try:
            # Проверяем, существует ли таблица пользователя
            check_table_sql = f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'prices' 
                AND table_name = '{username}'
            )
            """
            
            result = self.db.execute(text(check_table_sql)).scalar()
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Таблица цен для пользователя {username} не найдена"
                )
            
            # Вставляем данные в таблицу пользователя
            insert_sql = f"""
            INSERT INTO prices."{username}" (work_type_children_id, price)
            VALUES (:work_type_children_id, :price)
            ON CONFLICT (work_type_children_id) 
            DO UPDATE SET price = :price
            """
            
            self.db.execute(
                text(insert_sql),
                {
                    "work_type_children_id": work_type_children_id,
                    "price": price
                }
            )
            self.db.commit()
            
            return {
                "work_type_children_id": work_type_children_id,
                "price": price
            }
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при вставке данных в таблицу цен: {str(e)}"
            )

    def get_price_by_work_type(self, username: str, work_type_children_id: int):
        """
        Получает цену по типу работы для пользователя
        """
        try:
            # Проверяем, существует ли таблица пользователя
            check_table_sql = f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'prices' 
                AND table_name = '{username}'
            )
            """
            
            result = self.db.execute(text(check_table_sql)).scalar()
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Таблица цен для пользователя {username} не найдена"
                )
            
            # Получаем данные из таблицы пользователя
            select_sql = f"""
            SELECT work_type_children_id, price
            FROM prices."{username}"
            WHERE work_type_children_id = :work_type_children_id
            """
            
            result = self.db.execute(
                text(select_sql),
                {"work_type_children_id": work_type_children_id}
            ).fetchone()
            
            if result:
                return {
                    "work_type_children_id": result[0],
                    "price": float(result[1])
                }
            else:
                return None
                
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при получении данных из таблицы цен: {str(e)}"
            )