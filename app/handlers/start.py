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
    Handler for the /start command.

    Registers the user in the database and shows a welcome message
    with a button to check subscriptions.
    """
    tg_id = message.from_user.id
    username = message.from_user.username or ""

    await set_user(tg_id, username)

    await message.answer(
        "📹 The video with the school trash!\n\n"
        "Subscribe to all channels 👇 and get access to the forbidden content",
        reply_markup=get_check_sub_button(tg_id),
    )


@router.callback_query(F.data.startswith("check_subs:"))
async def handle_check_subscriptions(callback: CallbackQuery):
    """
    Checks the user's subscriptions to all required channels.

    If the user is subscribed to all channels, it shows the content.
    If not, it displays a list of channels to subscribe to.
    """
    tg_id = callback.from_user.id

    # Get the list of channels from the database
    async with async_session() as session:
        result = await session.execute(
            # ORM query to Channel
            Channel.__table__.select()
        )
        channels = [row.name for row in result.fetchall()]

    if not channels:
        await callback.message.answer("❌ No channels to check.")
        return await callback.answer()

    # Check subscriptions
    unsubscribed = await check_user_subscriptions(bot, tg_id, channels)

    if unsubscribed:
        await update_subscription_status(tg_id, False)
        await callback.message.answer(
            "🚫 You are not subscribed to these channels:",
            reply_markup=get_channels_buttons(unsubscribed)
        )
    else:
        await update_subscription_status(tg_id, True)
        text, keyboard = get_content_message()
        await callback.message.answer(text, reply_markup=keyboard)

    await callback.answer()  # close the "loading" clock


@router.message(Command("trash"))
async def handle_check_subscriptions(message: Message):
    """
    Checks the user's subscriptions to all required channels.

    If the user is subscribed to all channels, it shows the content.
    If not, it displays a list of channels to subscribe to.
    """
    tg_id = message.from_user.id

    # Get the list of channels from the database
    async with async_session() as session:
        result = await session.execute(
            # ORM query to Channel
            Channel.__table__.select()
        )
        channels = [row.name for row in result.fetchall()]

    if not channels:
        await message.answer("❌ No channels to check.")
        return

    # Check subscriptions
    unsubscribed = await check_user_subscriptions(bot, tg_id, channels)

    if unsubscribed:
        await update_subscription_status(tg_id, False)
        await message.answer(
            "🚫 You are not subscribed to these channels:",
            reply_markup=get_channels_buttons(unsubscribed)
        )
    else:
        await update_subscription_status(tg_id, True)
        text, keyboard = get_content_message()
        await message.answer(text, reply_markup=keyboard)
