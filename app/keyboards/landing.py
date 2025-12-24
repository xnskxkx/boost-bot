from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_content_message() -> tuple[str, InlineKeyboardMarkup]:
    """
    Возвращает финальный текст и клавиатуру с контентом.
    """
    text = (
        "💀 <b>ДОСТУП ОТКРЫТ!</b>\n\n"
        "Ты прошел проверку — теперь держи тот самый трэш 🔥\n"
        "Жми на кнопку и погрузись в ад 👇\n\n"
        "<i>Если не открывается — попробуй с телефона или обнови Telegram.</i>"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤯 СМОТРЕТЬ ТРЭШ",
                    url="https://t.me/your_private_channel_or_content"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💩 ВСТУПИТЬ В БЕСПРЕДЕЛ",
                    url="https://t.me/your_private_chat"
                )
            ]
        ]
    )

    return text, keyboard
