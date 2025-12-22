from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TELEGRAM_TOKEN


# Creating a bot instance
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
"""
Bot is the main object for interacting with the Telegram API.
The parse_mode parameter via DefaultBotProperties allows you to use
HTML tags (<b>, <i>, <u>, <a href="">, etc.) in all messages by default.
"""