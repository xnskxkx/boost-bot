from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Sequence


def get_check_sub_button(tg_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой 'Проверить подписку'.
    :param tg_id: добавляется в callback_data для уникальности.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔍 Проверить подписку",
                    callback_data=f"check_subs:{tg_id}"
                )
            ]
        ]
    )
    return keyboard


def get_channels_buttons(channels: Sequence[str]) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками для перехода на каналы (URL-кнопки).
    :param channels: список строк (например ['@ch1', '@ch2'])
    """
    buttons = []

    for ch in channels:
        channel_name = ch.replace("@", "")
        url = f"https://t.me/{channel_name}"
        buttons.append(
            [InlineKeyboardButton(text=f"📢 Подписаться на {ch}", url=url)]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
