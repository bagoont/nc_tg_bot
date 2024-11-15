"""Build dispatcher logic and bot instance.

Build dispatcher and bot instance for the Nextcloud Telegram Bot, configuringthe
storage backend and integrating with the Telegram API.
"""

from collections.abc import Callable
from typing import Any, cast

from aiogram import Bot, Dispatcher, loggers
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from bot.core.config import settings
from bot.db import session_maker

session = None
if settings.TG_API_SERVER:
    loggers.dispatcher.info("Bot works with self-hosted API server.")
    if settings.TG_LOCAL_MODE:
        loggers.dispatcher.info("Work with API in local mode.")
    session = AiohttpSession(
        api=TelegramAPIServer.from_base(settings.TG_API_SERVER, is_local=settings.TG_LOCAL_MODE),
    )

bot = Bot(
    token=settings.TG_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session,
)

_storage = (
    RedisStorage(
        redis=Redis(
            db=settings.redis.DB,
            host=settings.redis.HOSTNAME,
            password=settings.redis.PASSWORD,
            username=settings.redis.USERNAME,
            port=settings.redis.PORT,
        ),
    )
    if settings.redis
    else MemoryStorage()
)

dp = Dispatcher(storage=_storage, _session_maker=cast(Callable[[], Any], session_maker))
