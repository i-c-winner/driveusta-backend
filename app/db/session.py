import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Локально загружаем .env (на Render это не мешает)
load_dotenv()

# Берём DATABASE_URL из окружения
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not set. Please set DATABASE_URL environment variable for PostgreSQL connection.")

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Создаём фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
