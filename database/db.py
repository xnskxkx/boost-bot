import logging
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from config import DB_URL
from .models import Base


# Create DB engine: SQLite + aiosqlite (default for empty DB_URL)
engine = create_async_engine(
    url=DB_URL,
    echo=False,
    pool_pre_ping=True,
)

# Asynchronous session
# expire_on_commit=False → objects will not be invalidated immediately after commit
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


# =========================
#      INITIALIZATION
# =========================

async def init_db() -> None:
    """
    Create tables if they don't exist.
    Call from the entry point (run.py) when the bot starts.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logging.info(f"✅ Database initialized: {DB_URL}")
