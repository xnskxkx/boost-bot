import logging
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from config import DB_URL
from .models import Base


# Создание движка БД: SQLite + aiosqlite (дефолт на случай пустого DB_URL)
engine = create_async_engine(
    url=DB_URL,
    echo=False,
    pool_pre_ping=True,
)

# Асинхронная сессия
# expire_on_commit=False → объекты не будут инвалидироваться сразу после commit
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


# =========================
#      ИНИЦИАЛИЗАЦИЯ
# =========================

async def init_db() -> None:
    """
    Создать таблицы, если их нет.
    Вызывать из точки входа (run.py) при старте бота.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logging.info(f"✅ База данных инициализирована: {DB_URL}")
