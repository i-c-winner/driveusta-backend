#!/usr/bin/env python3
"""
Тестовый скрипт для проверки определения схем из моделей
"""

import os
import sys

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

def detect_schemas():
    """Обнаружить все схемы из моделей"""
    # Импортируем здесь, чтобы избежать проблем с зависимостями
    try:
        from app.db.base import Base
        import app.models
        import app.models.calendar
        
        schemas = set()
        target_metadata = Base.metadata
        
        print("Анализ таблиц:")
        for table_name, table in target_metadata.tables.items():
            print(f"  Таблица: {table_name}")
            
            # Проверяем атрибут __table_args__ у каждой таблицы
            if hasattr(table, '__table_args__'):
                table_args = table.__table_args__
                if table_args:
                    print(f"    __table_args__: {table_args}")
                    
                    # Если __table_args__ - словарь
                    if isinstance(table_args, dict):
                        if 'schema' in table_args:
                            schema_name = table_args['schema']
                            if schema_name:
                                schemas.add(schema_name)
                                print(f"      Найдена схема: {schema_name}")
                    # Если __table_args__ - кортеж
                    elif isinstance(table_args, tuple):
                        for arg in table_args:
                            if isinstance(arg, dict) and 'schema' in arg:
                                schema_name = arg['schema']
                                if schema_name:
                                    schemas.add(schema_name)
                                    print(f"      Найдена схема: {schema_name}")
                else:
                    print("    __table_args__ пустой или отсутствует")
            else:
                print("    Нет атрибута __table_args__")
        
        print("\nНайденные схемы:")
        for schema in sorted(schemas):
            print(f"  - {schema}")
        
        return schemas
    except Exception as e:
        print(f"Ошибка при импорте моделей: {e}")
        return set()

if __name__ == "__main__":
    schemas = detect_schemas()
    print(f"\nВсего найдено схем: {len(schemas)}")