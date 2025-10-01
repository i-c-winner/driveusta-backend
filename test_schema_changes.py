"""
Тестовый скрипт для проверки изменений схемы
"""
from sqlalchemy import create_engine, MetaData
from app.db.base import Base
from app.models.work_shops import WorkShop
from app.models.calendar.appointments import Appointments
from app.models.calendar.holidays import Holidays
from app.models.calendar.working_hours import WorkingHours
from app.models.avialableCars import AvialableCars
from app.models.photos import Photos
from app.models.type_work_children import TypeWorkChildren
from app.models.type_work_parents import TypeWorkParents
from app.models.addreses import Addresses
from app.models.streets import Streets
from app.models.participants import Participants
from app.models.cars import Cars

def test_schema():
    """Тест для проверки схемы"""
    print("Проверка схемы work_shop...")
    
    # Проверяем, что все модели имеют правильную схему
    work_shop_models = [
        ("work_shop", WorkShop),
        ("holidays", Holidays),
        ("working_hours", WorkingHours),
        ("avialable_cars", AvialableCars),
        ("photos", Photos),
    ]
    
    for name, model in work_shop_models:
        table = model.__table__
        schema = getattr(table, 'schema', None)
        print(f"Модель {name}: схема = {schema}")
        assert schema == "work_shop", f"Модель {name} должна иметь схему 'work_shop', но имеет '{schema}'"
    
    print("Все модели корректно используют схему 'work_shop'")
    
    # Проверяем модели в схеме participants
    print("\nПроверка схемы participants...")
    
    participants_models = [
        ("appointments", Appointments),
        ("participants", Participants),
    ]
    
    for name, model in participants_models:
        table = model.__table__
        schema = getattr(table, 'schema', None)
        print(f"Модель {name}: схема = {schema}")
        assert schema == "participants", f"Модель {name} должна иметь схему 'participants', но имеет '{schema}'"
    
    print("Все модели корректно используют схему 'participants'")
    
    # Проверяем модели в схеме cars
    print("\nПроверка схемы cars...")
    
    cars_models = [
        ("cars", Cars),
        ("type_work_children", TypeWorkChildren),
        ("type_work_parents", TypeWorkParents),
    ]
    
    for name, model in cars_models:
        table = model.__table__
        schema = getattr(table, 'schema', None)
        print(f"Модель {name}: схема = {schema}")
        assert schema == "cars", f"Модель {name} должна иметь схему 'cars', но имеет '{schema}'"
    
    print("Все модели корректно используют схему 'cars'")
    
    # Проверяем модели в схеме public, которые ссылаются на work_shop
    public_models = [
        ("addresses", Addresses),
        ("streets", Streets),
    ]
    
    for name, model in public_models:
        table = model.__table__
        schema = getattr(table, 'schema', None)
        print(f"Модель {name}: схема = {schema}")
        assert schema is None, f"Модель {name} должна иметь схему None (public), но имеет '{schema}'"
        
        # Проверяем внешние ключи
        for fk in table.foreign_keys:
            if 'work_shop' in str(fk.column):
                expected_ref = f"work_shop.work_shop.id"
                actual_ref = f"{fk.column.table.schema}.{fk.column.table.name}.{fk.column.name}"
                print(f"  Внешний ключ: {fk.parent.name} -> {actual_ref}")
                assert actual_ref == expected_ref, f"Внешний ключ должен ссылаться на '{expected_ref}', но ссылается на '{actual_ref}'"
    
    print("Все модели в схеме public корректно ссылаются на таблицы в схеме work_shop")
    
    # Проверяем связующие таблицы
    print("\nПроверка связующих таблиц...")
    from app.db.base import (
        holiday_work_shop,
        working_hour_work_shop,
        appointments_work_type_children,
        appointments_work_shop,
        appointments_cars
    )
    
    # Связующие таблицы в схеме work_shop
    work_shop_association_tables = [
        ("holidays_work_shops", holiday_work_shop),
        ("working_hour_work_shop", working_hour_work_shop),
    ]
    
    for name, table in work_shop_association_tables:
        schema = getattr(table, 'schema', None)
        print(f"Связующая таблица {name}: схема = {schema}")
        assert schema == "work_shop", f"Таблица {name} должна иметь схему 'work_shop', но имеет '{schema}'"
    
    # Связующие таблицы в схеме participants
    participants_association_tables = [
        ("appointments_work_type_children", appointments_work_type_children),
        ("appointments_work_shop", appointments_work_shop),
        ("appointments_cars", appointments_cars),
    ]
    
    for name, table in participants_association_tables:
        schema = getattr(table, 'schema', None)
        print(f"Связующая таблица {name}: схема = {schema}")
        assert schema == "participants", f"Таблица {name} должна иметь схему 'participants', но имеет '{schema}'"
    
    print("Все связующие таблицы корректно используют схемы 'work_shop' и 'participants'")
    
    # Проверяем внутренние связи в схемах
    print("\nПроверка внутренних связей в схемах...")
    
    # Проверяем связи в модели Appointments
    appointments_table = Appointments.__table__
    for fk in appointments_table.foreign_keys:
        expected_schemas = ["participants", "work_shop", "public", "cars"]
        actual_schema = fk.column.table.schema
        print(f"  Внешний ключ в appointments: appointments -> {actual_schema}.{fk.column.table.name}")
        assert actual_schema in expected_schemas, f"Внешний ключ в appointments должен ссылаться на схему из {expected_schemas}, но ссылается на '{actual_schema}'"
    
    # Проверяем связи в модели Participants
    participants_table = Participants.__table__
    for fk in participants_table.foreign_keys:
        if 'cars' in str(fk.column):
            expected_ref = f"cars.cars.id"
            actual_ref = f"{fk.column.table.schema}.{fk.column.table.name}.{fk.column.name}"
            print(f"  Внешний ключ в participants: participants -> {actual_ref}")
            assert actual_ref == expected_ref, f"Внешний ключ должен ссылаться на '{expected_ref}', но ссылается на '{actual_ref}'"
    
    # Проверяем связи в модели TypeWorkChildren
    type_work_children_table = TypeWorkChildren.__table__
    for fk in type_work_children_table.foreign_keys:
        expected_schemas = ["cars"]
        actual_schema = fk.column.table.schema
        print(f"  Внешний ключ в type_work_children: type_work_children -> {actual_schema}.{fk.column.table.name}")
        assert actual_schema in expected_schemas, f"Внешний ключ в type_work_children должен ссылаться на схему из {expected_schemas}, но ссылается на '{actual_schema}'"
    
    print("Все внутренние связи в схемах корректны")

if __name__ == "__main__":
    test_schema()
    print("\n✅ Все проверки пройдены успешно!")