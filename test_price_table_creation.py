#!/usr/bin/env python3
"""
Test script to verify the price table creation functionality
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up environment variables for testing
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/driveusta"

try:
    from app.api.v1.auth.register import create_token
    from fastapi.security import OAuth2PasswordRequestForm
    from app.db.session import engine
    from sqlalchemy import text
    
    print("Testing price table creation...")
    
    # Проверим, можем ли мы подключиться к базе данных
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print(f"Database connection successful: {result.fetchone()}")
        
        # Проверим существование схемы price
        result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'price'"))
        if result.fetchone():
            print("Schema 'price' exists")
        else:
            print("Schema 'price' does not exist")
    
    print("Test completed successfully!")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)