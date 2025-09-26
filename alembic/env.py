import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Локально загружаем .env (на Render это не мешает)
from dotenv import load_dotenv
load_dotenv()

# Импорт базы и моделей
from app.db.base import Base
import app.models  # чтобы Alembic видел все модели

# Настройка Alembic
config = context.config
fileConfig(config.config_file_name)

# Метаданные для автогенерации миграций
target_metadata = Base.metadata

# Берём DATABASE_URL из окружения
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not set")

# Функция для онлайн-миграций
def run_migrations_online():
    connectable = engine_from_config(
        {},
        url=DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Основной запуск
if context.is_offline_mode():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
else:
    run_migrations_online()
