import sqlalchemy
from sqlalchemy import text

def check_cars_schema():
    try:
        engine = sqlalchemy.create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/driveusta')
        with engine.connect() as conn:
            # Проверяем схему cars
            print("Проверка существования схемы cars...")
            result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'cars'"))
            schema = result.fetchone()
            if schema:
                print("✅ Схема 'cars' существует")
            else:
                print("❌ Схема 'cars' не найдена")
            
            # Проверяем таблицы в схеме cars
            print("\nПроверка таблиц в схеме cars:")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'cars' 
                ORDER BY table_name
            """))
            cars_tables = [row[0] for row in result]
            expected_tables = ['cars', 'type_work_children', 'type_work_parents']
            
            for table in expected_tables:
                if table in cars_tables:
                    print(f"✅ Таблица 'cars.{table}' существует")
                else:
                    print(f"❌ Таблица 'cars.{table}' не найдена")
            
            # Если схема cars не существует, проверим, где находятся таблицы
            if not schema:
                print("\nПроверка местоположения таблиц:")
                for table in expected_tables:
                    result = conn.execute(text(f"""
                        SELECT table_schema
                        FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    """))
                    row = result.fetchone()
                    if row:
                        print(f"Таблица '{table}' находится в схеме '{row[0]}'")
                    else:
                        print(f"Таблица '{table}' не найдена")
                
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check_cars_schema()