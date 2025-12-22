import logging
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from typing import Sequence

from database.repo import get_all_channels


async def check_user_subscriptions(bot: Bot, tg_id: int, channels: Sequence[str]) -> list[str]:
    """
    Check which channels from the list the user is not subscribed to.

    :param bot: an instance of aiogram.Bot
    :param tg_id: Telegram ID of the user
    :param channels: a list of channels (e.g., ["@mychannel1", "@mychannel2"])
    :return: a list of channels to which the user is NOT subscribed
    """
    unsubscribed_channels = []

    for channel in channels:
        try:
            member = await bot.get_chat_member(channel, tg_id)

            if member.status not in ("member", "administrator", "creator"):
                unsubscribed_channels.append(channel)

        except TelegramForbiddenError:
            # The bot does not have access to the channel (not added as an admin)
            logging.warning(f"⚠️ No rights to check channel {channel}")
            unsubscribed_channels.append(channel)

        except TelegramBadRequest as e:
            # Channel not found / incorrect name
            logging.warning(f"⚠️ Error checking {channel}: {e}")
            unsubscribed_channels.append(channel)

        except Exception as e:
            # Any other error
            logging.error(f"❌ Failed to check {channel}: {e}")
            unsubscribed_channels.append(channel)

    return unsubscribed_channels


async def get_channels_list() -> list[str]:
    """
    Get the list of channels from the database.
    """
    channels = await get_all_channels()
    return [c.name for c in channels]
