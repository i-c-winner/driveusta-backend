import sqlalchemy
from sqlalchemy import text

def check_schemas():
    try:
        engine = sqlalchemy.create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/driveusta')
        with engine.connect() as conn:
            # Проверяем схемы
            print("Проверка существующих схем...")
            result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('work_shop', 'participants', 'cars')"))
            schemas = [row[0] for row in result]
            print(f"Найденные схемы: {schemas}")
            
            # Проверяем таблицы в схеме work_shop
            print("\nТаблицы в схеме work_shop:")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'work_shop' 
                ORDER BY table_name
            """))
            work_shop_tables = [row[0] for row in result]
            for table in work_shop_tables:
                print(f"  - {table}")
            
            # Проверяем таблицы в схеме participants
            print("\nТаблицы в схеме participants:")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'participants' 
                ORDER BY table_name
            """))
            participants_tables = [row[0] for row in result]
            for table in participants_tables:
                print(f"  - {table}")
            
            # Проверяем таблицы в схеме cars
            print("\nТаблицы в схеме cars:")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'cars' 
                ORDER BY table_name
            """))
            cars_tables = [row[0] for row in result]
            for table in cars_tables:
                print(f"  - {table}")
            
            # Проверяем таблицы в схеме public
            print("\nТаблицы в схеме public:")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            public_tables = [row[0] for row in result]
            for table in public_tables:
                print(f"  - {table}")
                
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check_schemas()