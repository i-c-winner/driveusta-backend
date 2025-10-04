# Создание схем в PostgreSQL с помощью Alembic

## Обзор

В этом проекте используется PostgreSQL с несколькими схемами для организации таблиц. Для автоматического создания схем при запуске миграций были внесены следующие изменения:

## Структура миграций

1. **[0001_create_schemas.py](file:///Volumes/D/Documents/work/driveusta/driveusta_back/alembic/versions/0001_create_schemas.py)** - первая миграция, которая создает все необходимые схемы в базе данных
2. **[a0253e07a4ec_consolidate_tables.py](file:///Volumes/D/Documents/work/driveusta/driveusta_back/alembic/versions/a0253e07a4ec_consolidate_tables.py)** - последующие миграции, которые создают таблицы в соответствующих схемах

## Как это работает

### Автоматическое определение схем

Схемы определяются автоматически из атрибутов `__table_args__` моделей SQLAlchemy:

```python
class Cars(Base):
    __tablename__ = "cars"
    __table_args__ = {"schema": "cars"}  # Определяет схему
    
    id = Column(Integer, primary_key=True, index=True)
    # ... другие поля
```

### Используемые схемы

На основе анализа моделей определены следующие схемы:
- `cars` - для таблиц, связанных с автомобилями
- `participants` - для таблиц, связанных с участниками
- `work_shop` - для таблиц, связанных с мастерскими

### Создание схем

При запуске миграций схемы создаются автоматически двумя способами:

1. **Через миграцию [0001_create_schemas.py](file:///Volumes/D/Documents/work/driveusta/driveusta_back/alembic/versions/0001_create_schemas.py)** - при первом запуске миграций
2. **Через функцию [create_schemas_if_not_exist](file:///Volumes/D/Documents/work/driveusta/driveusta_back/alembic/env.py#L35-L72) в [env.py](file:///Volumes/D/Documents/work/driveusta/driveusta_back/alembic/env.py)** - при каждом запуске миграций

## Порядок выполнения миграций

```
0001_create_schemas.py → a0253e07a4ec_consolidate_tables.py → ...
```

Каждая последующая миграция зависит от предыдущей благодаря параметрам `down_revision`.

## Добавление новых схем

Чтобы добавить новую схему:

1. Добавьте атрибут `__table_args__ = {"schema": "new_schema_name"}` в модель
2. Обновите список схем в миграции [0001_create_schemas.py](file:///Volumes/D/Documents/work/driveusta/driveusta_back/alembic/versions/0001_create_schemas.py)
3. При следующем запуске миграций схема будет создана автоматически

## Запуск миграций

Для запуска миграций используйте одну из следующих команд:

```bash
# Применить все миграции
alembic upgrade head

# Применить одну миграцию
alembic upgrade +1

# Откатить все миграции
alembic downgrade base
```

## Проверка схем

Для проверки, какие схемы будут созданы, можно использовать скрипт [analyze_models.py](file:///Volumes/D/Documents/work/driveusta/driveusta_back/analyze_models.py):

```bash
python analyze_models.py
```

## Безопасность

- Схемы создаются с использованием `CREATE SCHEMA IF NOT EXISTS`, что предотвращает ошибки при повторном запуске
- В downgrade миграциях удаление схем закомментировано для предотвращения случайной потери данных