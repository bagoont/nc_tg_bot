"""Build dispatcher logic and bot instance.

Build dispatcher and bot instance for the Nextcloud Telegram Bot, configuringthe
storage backend and integrating with the Telegram API.
"""

import json
from typing import Any

from aiogram import Bot, Dispatcher, loggers
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from redis.asyncio import Redis

from bot.core import settings
from bot.utils import as_obj, default

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


if settings.redis:

    def _json_dumps(obj: Any) -> str:
        return json.dumps(obj, default=default)

    def _json_loads(obj: Any) -> Any:
        return json.loads(obj, object_hook=as_obj)

    _storage = RedisStorage(
        redis=Redis(
            db=settings.redis.DB,
            host=settings.redis.HOSTNAME,
            password=settings.redis.PASSWORD,
            username=settings.redis.USERNAME,
            port=settings.redis.PORT,
        ),
        key_builder=DefaultKeyBuilder(with_destiny=True),
        json_dumps=_json_dumps,
        json_loads=_json_loads,
    )
else:
    _storage = MemoryStorage()


dp = Dispatcher(storage=_storage)
