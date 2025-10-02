#!/usr/bin/env python3
"""
Тестовый скрипт для проверки создания схем
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_schema_creation():
    """Тест создания схем"""
    # Получаем URL базы данных
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ Не найдена переменная окружения DATABASE_URL")
        return False
    
    try:
        # Создаем подключение к базе данных
        engine = create_engine(database_url)
        
        # Подключаемся к базе данных
        with engine.connect() as connection:
            print("✅ Подключение к базе данных успешно")
            
            # Список схем для создания
            schemas = ['cars', 'participants', 'work_shop']
            
            # Создаем каждую схему
            for schema in schemas:
                if schema != 'public':
                    try:
                        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                        print(f"✅ Создана схема: {schema}")
                    except Exception as e:
                        print(f"⚠️  Ошибка при создании схемы {schema}: {e}")
            
            # Проверяем существующие схемы
            result = connection.execute(text("SELECT schema_name FROM information_schema.schemata"))
            existing_schemas = [row[0] for row in result]
            
            print("\nСуществующие схемы в базе данных:")
            for schema in sorted(existing_schemas):
                print(f"  - {schema}")
            
            # Проверяем, созданы ли наши схемы
            print("\nПроверка созданных схем:")
            for schema in schemas:
                if schema in existing_schemas:
                    print(f"✅ Схема {schema} существует")
                else:
                    print(f"❌ Схема {schema} отсутствует")
            
            return True
            
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False

if __name__ == "__main__":
    print("Тест создания схем в PostgreSQL")
    print("=" * 40)
    
    success = test_schema_creation()
    
    if success:
        print("\n✅ Тест пройден успешно")
    else:
        print("\n❌ Тест не пройден")
        sys.exit(1)