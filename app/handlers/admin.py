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
    Показать статистику бота (только для администратора).

    Выводит количество пользователей, подписок и другие метрики.
    """
    if message.from_user.id != USER_ID_FOR_ADMIN:
        return await message.answer("Нет доступа")

    data = await get_stats()
    await message.answer(format_stats(data))


@router.message(Command("addchannel"))
async def add_channel(message: Message):
    """
    Добавить канал в список для отслеживания подписок (только для администратора).

    Формат: /addchannel @channel_name
    """
    tg_id = message.from_user.id
    if tg_id != USER_ID_FOR_ADMIN:
        return await message.answer("🚫 Нет доступа")

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Укажи название канала, например:\n/addchannel @mychannel")

    channel_name = parts[1].strip()

    async with async_session() as session:
        exists = await session.scalar(Channel.__table__.select().where(Channel.name == channel_name))
        if exists:
            return await message.answer("⚠️ Этот канал уже есть в списке.")

        session.add(Channel(name=channel_name))
        await session.commit()

    await message.answer(f"✅ Канал {channel_name} добавлен.")