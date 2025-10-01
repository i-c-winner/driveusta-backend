import sqlalchemy
from sqlalchemy import text

def verify_tables():
    try:
        engine = sqlalchemy.create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/driveusta')
        with engine.connect() as conn:
            # Проверяем схемы
            result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'work_shop'"))
            row = result.fetchone()
            if row:
                print("✅ Схема 'work_shop' существует")
            else:
                print("❌ Схема 'work_shop' не найдена")
            
            # Проверяем таблицы в схеме work_shop
            work_shop_tables = [
                'appointments', 'holidays', 'type_work_parents', 'work_shop',
                'avialable_cars', 'holidays_work_shops', 'photos', 'type_work_children',
                'working_hours', 'appointments_cars', 'appointments_work_shop',
                'appointments_work_type_children', 'working_hour_work_shop'
            ]
            
            for table in work_shop_tables:
                result = conn.execute(text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'work_shop' AND table_name = '{table}'"))
                row = result.fetchone()
                if row:
                    print(f"✅ Таблица 'work_shop.{table}' существует")
                else:
                    print(f"❌ Таблица 'work_shop.{table}' не найдена")
            
            # Проверяем таблицы в схеме public
            public_tables = ['cars', 'addresses', 'participants', 'streets']
            
            for table in public_tables:
                result = conn.execute(text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{table}'"))
                row = result.fetchone()
                if row:
                    print(f"✅ Таблица 'public.{table}' существует")
                else:
                    print(f"❌ Таблица 'public.{table}' не найдена")
            
            # Проверяем внешние ключи
            print("\nПроверка внешних ключей...")
            result = conn.execute(text("""
                SELECT 
                    tc.table_name, 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu 
                      ON tc.constraint_name = kcu.constraint_name 
                      AND tc.table_schema = kcu.table_schema 
                    JOIN information_schema.constraint_column_usage AS ccu 
                      ON ccu.constraint_name = tc.constraint_name 
                      AND ccu.table_schema = tc.table_schema 
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                  AND tc.table_name IN ('addresses', 'streets') 
                  AND tc.table_schema = 'public'
            """))
            
            for row in result:
                print(f"✅ Внешний ключ: {row[0]}.{row[1]} -> {row[2]}.{row[3]}")
                
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    verify_tables()