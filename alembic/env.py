import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Локально загружаем .env
from dotenv import load_dotenv
load_dotenv()

# Импорт базы и моделей
from app.db.base import Base
import app.models  # чтобы Alembic видел все модели
import app.models.calendar  # чтобы Alembic видел все модели календаря

# Настройка Alembic
config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")

if DATABASE_URL and DATABASE_URL.startswith("DATABASE_URL="):
    DATABASE_URL = DATABASE_URL.split("=", 1)[1].strip()

if not DATABASE_URL or DATABASE_URL.startswith("driver://"):
    raise ValueError(f"❌ No valid database URL. Got: {DATABASE_URL!r}")

# --- OFFLINE ---
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        include_schemas=True,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

# --- ONLINE ---
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,   # 🔥 важно
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

# Основной запуск
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
