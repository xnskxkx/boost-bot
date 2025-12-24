import asyncio
import logging
from aiogram import Dispatcher

from app.client import bot
from database.db import init_db
from app.handlers import admin, start


async def main():
    """
    Точка входа в бота.
    """
    # Инициализация базы данных
    await init_db()

    # Создаём диспетчер
    dp = Dispatcher()

    # Подключаем все роутеры
    dp.include_router(admin.router)
    dp.include_router(start.router)

    # Удаляем старый webhook (если был)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("🤖 Бот запущен. Ожидание сообщений...")

    # Запуск long polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("👋 Завершение работы бота")
