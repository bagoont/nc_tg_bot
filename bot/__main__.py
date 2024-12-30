import logging

import uvloop
from nc_py_api import AsyncNextcloud
from redis.asyncio import Redis
from sqlalchemy import select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from bot.core import bot, dp, on_shutdown, on_startup, settings, webhook_run
from bot.db import session_maker

MAX_TRIES = 6
WAIT_SECONDS = 5

logger = logging.getLogger("aiogram.dispatcher")


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARNING),
)
async def check_db_connection() -> None:
    if not settings.db:
        return
    async with session_maker() as session:
        await session.execute(select(1))


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARNING),
    reraise=True,
)
async def check_nc_capabilities(nc: AsyncNextcloud) -> None:
    await nc.capabilities


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARNING),
)
async def check_redis_connection() -> None:
    if not settings.redis:
        return
    redis = Redis(
        host=settings.redis.HOSTNAME,
        port=settings.redis.PORT,
        db=settings.redis.DB,
        username=settings.redis.USERNAME,
        password=settings.redis.PASSWORD,
    )
    await redis.ping()


async def main() -> None:
    """Asynchronous entry point for the application.

    This function initializes the bot, registers event handlers,
    and starts the polling process or webhook, depending on the configuration settings.
    """
    nc = AsyncNextcloud(nextcloud_url=f"{settings.nc.SCHEME}://{settings.nc.HOST}:{settings.nc.PORT}")
    await check_nc_capabilities(nc)
    if settings.db:
        await check_db_connection()
    if settings.redis:
        await check_redis_connection()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    if settings.webhook:
        await webhook_run(
            dp,
            bot,
            settings.webhook.BASEURL,
            settings.webhook.PATH,
            settings.webhook.HOST,
            settings.webhook.PORT,
            settings.webhook.SECRET,
        )
    else:
        await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(settings.LOG_LEVEL))

    uvloop.run(main())
