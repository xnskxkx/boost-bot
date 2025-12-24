from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Sequence


def get_check_sub_button(tg_id: int) -> InlineKeyboardMarkup:
    """
    Keyboard with a 'Check Subscription' button.
    :param tg_id: added to callback_data for uniqueness.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔍 Check Subscription",
                    callback_data=f"check_subs:{tg_id}"
                )
            ]
        ]
    )
    return keyboard


def get_channels_buttons(channels: Sequence[str]) -> InlineKeyboardMarkup:
    """
    Keyboard with buttons to go to channels (URL buttons).
    :param channels: list of strings (e.g., ['@ch1', '@ch2'])
    """
    buttons = []

    for ch in channels:
        channel_name = ch.replace("@", "")
        url = f"https://t.me/{channel_name}"
        buttons.append(
            [InlineKeyboardButton(text=f"📢 Subscribe to {ch}", url=url)]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
