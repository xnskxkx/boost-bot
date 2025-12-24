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
    Find a user by tg_id or create a new one.
    Updates the username if it has changed.
    """
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            if user:
                # update username on change
                if username and user.username != username:
                    user.username = username
                    await session.commit()
                    await session.refresh(user)
                return user

            # create a new user
            user = User(tg_id=tg_id, username=username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

        except SQLAlchemyError as e:
            logging.error(f"❌ Error in get_or_create_user: {e}")
            return None


async def set_user(tg_id: int, username: str | None) -> None:
    """
    Idempotent user registration:
    if exists - updates username (if changed);
    if not - creates.
    """
    await get_or_create_user(tg_id, username)


async def update_subscription_status(tg_id: int, is_subscribed: bool) -> None:
    """
    Update user's subscription status.
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
    Get user statistics:
    total, subscribed, unsubscribed.
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
    Get all users.
    """
    async with async_session() as session:
        result = await session.scalars(select(User))
        return list(result.all())


# =========================
#        CHANNELS
# =========================

async def get_all_channels() -> list[User]:
    """
    Get all channels.
    """
    async with async_session() as session:
        result = await session.scalars(select(Channel))
        return list(result.all())

