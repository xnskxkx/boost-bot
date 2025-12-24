import asyncio
import logging
from aiogram import Dispatcher

from app.client import bot
from database.db import init_db
from app.handlers import admin, start


async def main():
    """
    Bot entry point.
    """
    # Initialize the database
    await init_db()

    # Create a dispatcher
    dp = Dispatcher()

    # Connect all routers
    dp.include_router(admin.router)
    dp.include_router(start.router)

    # Delete the old webhook (if it existed)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("🤖 Bot started. Waiting for messages...")

    # Start long polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("👋 Shutting down the bot")
