# Настройка базы данных PostgreSQL

## Переменные окружения

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/driveusta
```

## Настройка PostgreSQL

1. Установите PostgreSQL
2. Создайте базу данных:
   ```sql
   CREATE DATABASE driveusta;
   ```
3. Создайте пользователя (опционально):
   ```sql
   CREATE USER driveusta_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE driveusta TO driveusta_user;
   ```

## Схема базы данных

В проекте используется несколько схем базы данных:
- `public` - основная схема для общих таблиц
- `work_shop` - схема для таблиц, связанных с мастерскими
- `participants` - схема для таблиц, связанных с клиентами и записями
- `cars` - схема для таблиц, связанных с автомобилями

Таблицы в схеме `work_shop`:
- work_shop
- holidays
- working_hours
- avialable_cars
- photos

Таблицы в схеме `participants`:
- appointments
- participants

Таблицы в схеме `cars`:
- cars
- type_work_children
- type_work_parents

## Календарь

Система календаря включает три основные таблицы, связанные с мастерскими:
- `appointments` - Записи клиентов на прием
- `holidays` - Праздничные дни мастерской
- `working_hours` - Рабочие часы мастерской

Все записи календаря связаны с конкретной мастерской через поле `work_shop_id`.

## Применение миграций

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate

# Примените миграции
alembic upgrade head
```

## Запуск приложения

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate

# Запустите сервер
uvicorn app.main:app --reload
```

## API эндпоинты

### Эндпоинты для работы с СТО

- `POST /api/v1/work_shop/` - Создание нового СТО
- `GET /api/v1/work_shop/` - Получение списка всех СТО
- `GET /api/v1/work_shop/{id}` - Получение СТО по ID
- `GET /api/v1/work_shop/by-address/?street_name={street}&address={address}` - Получение СТО по адресу

### Эндпоинты календаря

- `POST /api/v1/calendar/appointments/` - Создание записи на прием
- `GET /api/v1/calendar/appointments/?work_shop_id={id}` - Получение всех записей на прием для СТО
- `GET /api/v1/calendar/appointments/{id}?work_shop_id={id}` - Получение записи на прием по ID
- `PUT /api/v1/calendar/appointments/{id}?work_shop_id={id}` - Обновление записи на прием
- `DELETE /api/v1/calendar/appointments/{id}?work_shop_id={id}` - Удаление записи на прием

- `POST /api/v1/calendar/holidays/` - Создание праздничного дня
- `GET /api/v1/calendar/holidays/?work_shop_id={id}` - Получение всех праздничных дней для СТО
- `GET /api/v1/calendar/holidays/{id}?work_shop_id={id}` - Получение праздничного дня по ID
- `PUT /api/v1/calendar/holidays/{id}?work_shop_id={id}` - Обновление праздничного дня
- `DELETE /api/v1/calendar/holidays/{id}?work_shop_id={id}` - Удаление праздничного дня

- `POST /api/v1/calendar/working-hours/` - Создание рабочих часов
- `GET /api/v1/calendar/working-hours/?work_shop_id={id}` - Получение всех рабочих часов для СТО
- `GET /api/v1/calendar/working-hours/{id}?work_shop_id={id}` - Получение рабочих часов по ID
- `PUT /api/v1/calendar/working-hours/{id}?work_shop_id={id}` - Обновление рабочих часов
- `DELETE /api/v1/calendar/working-hours/{id}?work_shop_id={id}` - Удаление рабочих часов