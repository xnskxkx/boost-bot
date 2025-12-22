from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TELEGRAM_TOKEN


# Создание экземпляра бота
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
"""
Bot — основной объект взаимодействия с Telegram API.
Параметр parse_mode через DefaultBotProperties позволяет использовать 
HTML-теги (<b>, <i>, <u>, <a href=""> и т. д.) во всех сообщениях по умолчанию.
"""