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
