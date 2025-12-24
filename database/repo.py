import logging
from sqlalchemy import select, func, update
from sqlalchemy.exc import SQLAlchemyError

from database.db import async_session
from database.models import User, Channel


# =========================
#        USERS
# =========================

async def get_or_create_user(tg_id: int, username: str | None) -> User:
    """
    Найти пользователя по tg_id или создать нового.
    Обновляет username, если он изменился.
    """
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            if user:
                # обновляем username при изменении
                if username and user.username != username:
                    user.username = username
                    await session.commit()
                    await session.refresh(user)
                return user

            # создаём нового пользователя
            user = User(tg_id=tg_id, username=username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

        except SQLAlchemyError as e:
            logging.error(f"❌ Ошибка при get_or_create_user: {e}")
            return None


async def set_user(tg_id: int, username: str | None) -> None:
    """
    Идемпотентная регистрация пользователя:
    если уже есть — обновляет username (если изменился);
    если нет — создаёт.
    """
    await get_or_create_user(tg_id, username)


async def update_subscription_status(tg_id: int, is_subscribed: bool) -> None:
    """
    Обновить статус подписки пользователя.
    """
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(is_subscribed=is_subscribed)
        )
        await session.commit()


async def get_stats() -> dict:
    """
    Получить статистику пользователей:
    всего, подписанных, неподписанных.
    """
    async with async_session() as session:
        total = await session.scalar(select(func.count()).select_from(User))
        subscribed = await session.scalar(
            select(func.count()).select_from(User).where(User.is_subscribed == True)
        )
        unsubscribed = (total or 0) - (subscribed or 0)

        return {
            "total": total or 0,
            "subscribed": subscribed or 0,
            "unsubscribed": unsubscribed or 0,
        }


async def get_all_users() -> list[User]:
    """
    Получить всех пользователей.
    """
    async with async_session() as session:
        result = await session.scalars(select(User))
        return list(result.all())


# =========================
#        CHANNELS
# =========================

async def get_all_channels() -> list[User]:
    """
    Получить все каналы.
    """
    async with async_session() as session:
        result = await session.scalars(select(Channel))
        return list(result.all())

