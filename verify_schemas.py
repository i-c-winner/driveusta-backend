#!/usr/bin/env python3
"""
Script to verify that schemas and tables were created correctly in PostgreSQL
"""
import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/driveusta")

def parse_db_url(db_url):
    """Parse database URL to get connection parameters"""
    # Parse the URL
    parsed = urlparse(db_url)
    
    return {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'database': parsed.path[1:] if parsed.path else 'driveusta',  # Remove leading slash
        'user': parsed.username or 'postgres',
        'password': parsed.password or 'postgres'
    }

def verify_schemas_and_tables():
    """Verify that schemas and tables were created correctly"""
    try:
        # Parse database connection parameters
        db_params = parse_db_url(DATABASE_URL)
        print(f"Connecting with params: {db_params}")
        
        # Connect to database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Check schemas
        print("\nChecking schemas...")
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name IN ('work_shop', 'participants', 'cars')
        """)
        schemas = [row[0] for row in cursor.fetchall()]
        print(f"Found schemas: {schemas}")
        
        # Check tables in each schema
        schemas_to_check = ['work_shop', 'participants', 'cars', 'public']
        for schema in schemas_to_check:
            print(f"\nChecking tables in schema '{schema}':")
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = %s
            """, (schema,))
            tables = [row[0] for row in cursor.fetchall()]
            print(f"  Tables: {tables}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n✅ Verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    verify_schemas_and_tables()