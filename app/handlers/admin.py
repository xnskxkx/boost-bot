from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import USER_ID_FOR_ADMIN
from database.repo import get_stats
from database.db import async_session
from database.models import Channel

from app.services.utils import format_stats

router = Router()


@router.message(Command("stats"))
async def stats(message: Message):
    """
    Show bot statistics (admin only).

    Displays the number of users, subscriptions, and other metrics.
    """
    if message.from_user.id != USER_ID_FOR_ADMIN:
        return await message.answer("Access denied")

    data = await get_stats()
    await message.answer(format_stats(data))


@router.message(Command("addchannel"))
async def add_channel(message: Message):
    """
    Add a channel to the subscription tracking list (admin only).

    Format: /addchannel @channel_name
    """
    tg_id = message.from_user.id
    if tg_id != USER_ID_FOR_ADMIN:
        return await message.answer("🚫 Access denied")

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Specify the channel name, for example:\n/addchannel @mychannel")

    channel_name = parts[1].strip()

    async with async_session() as session:
        exists = await session.scalar(Channel.__table__.select().where(Channel.name == channel_name))
        if exists:
            return await message.answer("⚠️ This channel is already on the list.")

        session.add(Channel(name=channel_name))
        await session.commit()

    await message.answer(f"✅ Channel {channel_name} added.")