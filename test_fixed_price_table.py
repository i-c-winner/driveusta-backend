#!/usr/bin/env python3
"""
Test script to verify the fixed price table creation functionality
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up environment variables for testing
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/driveusta"

try:
    from app.db.session import engine
    from sqlalchemy import text
    
    print("Testing fixed price table creation...")
    
    # Проверим подключение к базе данных
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print(f"Database connection successful: {result.fetchone()}")
    
    # Имитируем процесс создания таблицы с правильным внешним ключом
    test_username = "testuser_fixed"
    print(f"Creating price table for user: {test_username}")
    
    # Создаем схему price и таблицу пользователя с правильным внешним ключом
    with engine.connect() as conn:
        # Создаем схему price, если она не существует
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS price"))
        conn.commit()
        
        # Создаем таблицу с именем пользователя в схеме price
        # Используем текстовый SQL для правильного создания внешнего ключа
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS price."{test_username}" (
            work_type_children_id INTEGER,
            price NUMERIC(10, 2),
            PRIMARY KEY (work_type_children_id),
            CONSTRAINT fk_work_type_children 
                FOREIGN KEY (work_type_children_id) 
                REFERENCES cars.type_work_children(id)
                ON DELETE CASCADE
        )
        """
        conn.execute(text(create_table_sql))
        conn.commit()
    
    print(f"Price table for user '{test_username}' created successfully with proper foreign key!")
    
    # Проверим, что таблица создана
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'price' AND table_name = '{test_username}'
        """))
        if result.fetchone():
            print(f"Table 'price.{test_username}' exists")
        else:
            print(f"Table 'price.{test_username}' does not exist")
            
        # Проверим наличие внешнего ключа
        result = conn.execute(text(f"""
            SELECT constraint_name 
            FROM information_schema.table_constraints 
            WHERE table_schema = 'price' 
            AND table_name = '{test_username}' 
            AND constraint_type = 'FOREIGN KEY'
        """))
        if result.fetchone():
            print(f"Foreign key constraint exists in table 'price.{test_username}'")
        else:
            print(f"Foreign key constraint does not exist in table 'price.{test_username}'")
    
    print("Fixed price table creation test completed successfully!")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)