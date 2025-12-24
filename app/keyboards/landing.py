from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_content_message() -> tuple[str, InlineKeyboardMarkup]:
    """
    Returns the final text and keyboard with content.
    """
    text = (
        "💀 <b>ACCESS GRANTED!</b>\n\n"
        "You have passed the check - now here is the promised content 🔥\n"
        "Click the button and dive in 👇\n\n"
        "<i>If it doesn't open, try from your phone or update Telegram.</i>"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤯 WATCH CONTENT",
                    url="https://t.me/your_private_channel_or_content"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💩 JOIN THE MAYHEM",
                    url="https://t.me/your_private_chat"
                )
            ]
        ]
    )

    return text, keyboard
