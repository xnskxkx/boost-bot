import logging
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from typing import Sequence

from database.repo import get_all_channels


async def check_user_subscriptions(bot: Bot, tg_id: int, channels: Sequence[str]) -> list[str]:
    """
    Проверить, на какие каналы из списка пользователь не подписан.

    :param bot: экземпляр aiogram.Bot
    :param tg_id: Telegram ID пользователя
    :param channels: список каналов (например ["@mychannel1", "@mychannel2"])
    :return: список каналов, на которые пользователь НЕ подписан
    """
    unsubscribed_channels = []

    for channel in channels:
        try:
            member = await bot.get_chat_member(channel, tg_id)

            if member.status not in ("member", "administrator", "creator"):
                unsubscribed_channels.append(channel)

        except TelegramForbiddenError:
            # Бот не имеет доступа к каналу (не добавлен как админ)
            logging.warning(f"⚠️ Нет прав на проверку канала {channel}")
            unsubscribed_channels.append(channel)

        except TelegramBadRequest as e:
            # Канал не найден / некорректное имя
            logging.warning(f"⚠️ Ошибка проверки {channel}: {e}")
            unsubscribed_channels.append(channel)

        except Exception as e:
            # Любая другая ошибка
            logging.error(f"❌ Не удалось проверить {channel}: {e}")
            unsubscribed_channels.append(channel)

    return unsubscribed_channels


async def get_channels_list() -> list[str]:
    """
    Получить список каналов из БД (если хранить в таблице).
    """
    channels = await get_all_channels()
    return [c.name for c in channels]
