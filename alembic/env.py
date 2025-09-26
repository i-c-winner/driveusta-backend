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

# Берём DATABASE_URL из окружения, иначе из alembic.ini -> sqlalchemy.url
DATABASE_URL = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
print(DATABASE_URL, 'Dtabase URL')
if not DATABASE_URL or DATABASE_URL.startswith("driver://"):
    raise ValueError(
        "No valid database URL. Set DATABASE_URL env or configure sqlalchemy.url in alembic.ini"
    )

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

# Поддержка offline/online режимов
def run_migrations_offline():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

# Основной запуск
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
