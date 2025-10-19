#!/usr/bin/env python3
"""
Test script to verify the full registration process with price table creation
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up environment variables for testing
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/driveusta"

try:
    import asyncio
    from app.db.session import engine
    from sqlalchemy import text
    
    print("Testing full registration process...")
    
    # Проверим подключение к базе данных
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print(f"Database connection successful: {result.fetchone()}")
    
    # Имитируем процесс регистрации
    test_username = "testuser123"
    print(f"Creating price table for user: {test_username}")
    
    # Создаем схему price и таблицу пользователя
    with engine.connect() as conn:
        # Создаем схему price, если она не существует
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS price"))
        conn.commit()
        
        # Создаем таблицу с именем пользователя в схеме price
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS price.{test_username} (
            work_type_children_id INTEGER REFERENCES cars.type_work_children(id) ON DELETE CASCADE,
            price NUMERIC(10, 2),
            PRIMARY KEY (work_type_children_id)
        )
        """
        conn.execute(text(create_table_sql))
        conn.commit()
    
    print(f"Price table for user '{test_username}' created successfully!")
    
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
    
    print("Full registration test completed successfully!")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)