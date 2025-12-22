from __future__ import annotations
from datetime import datetime

from sqlalchemy import BigInteger, String, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


# --- Metadata settings (clean constraint and index names) ---
metadata = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models."""
    metadata = metadata


# =========================
#          MODELS
# =========================

class User(Base):
    """
    Bot user model.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_subscribed: Mapped[bool] = mapped_column(default=False)
    last_check: Mapped[datetime | None] = mapped_column(nullable=True)


class Channel(Base):
    """
    Channel model for tracking subscriptions.
    """
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    added_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
