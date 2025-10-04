# Руководство по миграции на новые схемы

## Обзор изменений

В рамках рефакторинга базы данных были внесены следующие изменения:

1. Создана новая схема `work_shop` в базе данных PostgreSQL
2. Следующие таблицы были перемещены в схему `work_shop`:
   - holidays
   - working_hours
   - avialable_cars
   - photos
   - type_work_children
   - type_work_parents
   - work_shop
3. Создана новая схема `participants` в базе данных PostgreSQL
4. Следующие таблицы были перемещены в схему `participants`:
   - appointments
   - participants
5. Все связующие таблицы также перемещены в соответствующие схемы:
   - holidays_work_shops (в work_shop)
   - working_hour_work_shop (в work_shop)
   - appointments_work_type_children (в participants)
   - appointments_work_shop (в participants)
   - appointments_cars (в participants)

## Изменения в моделях SQLAlchemy

Все модели были обновлены для использования новых схем:

```python
// Для таблиц в схеме work_shop
class Appointments(Base):
    __tablename__ = "appointments"
    __table_args__ = {"schema": "work_shop"}

// Для таблиц в схеме participants
class Appointments(Base):
    __tablename__ = "appointments"
    __table_args__ = {"schema": "participants"}
```

## Изменения в внешних ключах

Все внешние ключи были обновлены для корректной работы с новыми схемами:

```python
// Ранее
work_shop_id = Column(Integer, ForeignKey("work_shop.id"))

// Теперь для ссылки на таблицы в схеме work_shop
work_shop_id = Column(Integer, ForeignKey("work_shop.work_shop.id"))

// Для ссылки на таблицы в схеме participants
appointments_id = Column(Integer, ForeignKey("participants.appointments.id"))
```

Также обновлены внешние ключи в таблицах, которые остаются в схеме `public`, но ссылаются на таблицы в схеме `work_shop`:
- addresses
- streets

## Миграции Alembic

Были созданы миграции:

1. `37bae0e233b3_create_all_tables.py` - создает все таблицы в правильных схемах
2. `d8fdb4733d6f_move_appointments_and_participants_to_.py` - перемещает таблицы appointments и participants в новую схему participants

## Применение миграций

Для применения миграций выполните:

```bash
alembic upgrade head
```

## Откат миграций

Для отката миграций выполните:

```bash
alembic downgrade -1
```

Или для полного отката:

```bash
alembic downgrade base
```

## Проверка изменений

Для проверки корректности изменений можно запустить тестовый скрипт:

```bash
python test_schema_changes.py
```

## Возможные проблемы

1. **Ошибки внешних ключей**: Убедитесь, что все внешние ключи корректно обновлены
2. **Проблемы с доступом к таблицам**: При запросах к таблицам в новых схемах используйте полное имя: `schema.table_name`
3. **Ошибки миграций**: При возникновении ошибок миграции проверьте логи и при необходимости откатите изменения

## Обратная совместимость

Эти изменения ломают обратную совместимость с предыдущей структурой базы данных. Убедитесь, что:
1. Все разработчики обновили свои локальные копии кода
2. Продуктовая база данных будет обновлена перед развертыванием
3. Все связанные сервисы протестированы с новыми схемами