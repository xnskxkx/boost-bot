from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from app.keyboards.keyboards import get_check_sub_button, get_channels_buttons
from app.services.check_subs import check_user_subscriptions
from database.repo import set_user, update_subscription_status
from app.keyboards.landing import get_content_message
from database.db import async_session
from database.models import Channel
from app.client import bot

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    """
    Обработка команды /start.

    Регистрирует пользователя в базе и показывает приветственное сообщение
    с кнопкой для проверки подписок.
    """
    tg_id = message.from_user.id
    username = message.from_user.username or ""

    await set_user(tg_id, username)

    await message.answer(
        "📹 То самое видео с трэшем в школе!\n\n"
        "Подпишись на все каналы 👇 и получи доступ к запретке",
        reply_markup=get_check_sub_button(tg_id),
    )


@router.callback_query(F.data.startswith("check_subs:"))
async def handle_check_subscriptions(callback: CallbackQuery):
    """
    Проверка подписок пользователя на все обязательные каналы.

    Если пользователь подписан на все каналы — показывает контент.
    Если нет — выводит список каналов, на которые нужно подписаться.
    """
    tg_id = callback.from_user.id

    # Получаем список каналов из базы
    async with async_session() as session:
        result = await session.execute(
            # ORM-запрос к Channel
            Channel.__table__.select()
        )
        channels = [row.name for row in result.fetchall()]

    if not channels:
        await callback.message.answer("❌ Нет каналов для проверки.")
        return await callback.answer()

    # Проверяем подписки
    unsubscribed = await check_user_subscriptions(bot, tg_id, channels)

    if unsubscribed:
        await update_subscription_status(tg_id, False)
        await callback.message.answer(
            "🚫 Ты не подписан на эти каналы:",
            reply_markup=get_channels_buttons(unsubscribed)
        )
    else:
        await update_subscription_status(tg_id, True)
        text, keyboard = get_content_message()
        await callback.message.answer(text, reply_markup=keyboard)

    await callback.answer()  # закрываем "часики"


@router.message(Command("trash"))
async def handle_check_subscriptions(message: Message):
    """
    Проверка подписок пользователя на все обязательные каналы.

    Если пользователь подписан на все каналы — показывает контент.
    Если нет — выводит список каналов, на которые нужно подписаться.
    """
    tg_id = message.from_user.id

    # Получаем список каналов из базы
    async with async_session() as session:
        result = await session.execute(
            # ORM-запрос к Channel
            Channel.__table__.select()
        )
        channels = [row.name for row in result.fetchall()]

    if not channels:
        await message.answer("❌ Нет каналов для проверки.")
        return

    # Проверяем подписки
    unsubscribed = await check_user_subscriptions(bot, tg_id, channels)

    if unsubscribed:
        await update_subscription_status(tg_id, False)
        await message.answer(
            "🚫 Ты не подписан на эти каналы:",
            reply_markup=get_channels_buttons(unsubscribed)
        )
    else:
        await update_subscription_status(tg_id, True)
        text, keyboard = get_content_message()
        await message.answer(text, reply_markup=keyboard)
