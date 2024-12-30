"""Functions to handle bot startup, shutdown, and webhook operations."""

import asyncio

from aiogram import Bot, Dispatcher, loggers
from aiogram.enums import MenuButtonType
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs
from aiohttp.web import Application, AppRunner, TCPSite

from bot import dialogs, handlers
from bot.core import settings
from bot.db import session_maker
from bot.middlewares import DatabaseMD
from bot.utils import Commands


async def set_menu_button(bot: Bot) -> None:
    if settings.nc.BASEURL.startswith("https"):
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                type=MenuButtonType.WEB_APP,
                text="Nextcloud",
                web_app=WebAppInfo(
                    url=settings.nc.BASEURL,
                ),
            ),
        )


async def set_bot_menu(bot: Bot) -> None:
    await set_menu_button(bot)

    await bot.set_my_commands([command.value for command in Commands])


async def on_startup(dispatcher: Dispatcher, bot: Bot) -> None:
    loggers.dispatcher.info("Bot starting...")

    dispatcher.update.outer_middleware(DatabaseMD(session_maker))
    dispatcher.message.middleware(ChatActionMiddleware())

    await set_bot_menu(bot)

    setup_dialogs(dispatcher)

    for router in handlers.routers:
        dispatcher.include_router(router)
    for router in dialogs.routers:
        dispatcher.include_router(router)

    loggers.dispatcher.info("Bot started.")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    loggers.dispatcher.info("Bot stopping...")

    await dispatcher.storage.close()
    await dispatcher.fsm.storage.close()

    await bot.delete_webhook(drop_pending_updates=settings.TG_DROP_PENDING_UPDATES)
    await bot.session.close()

    loggers.dispatcher.info("Bot stopped.")


async def webhook_run(
    dp: Dispatcher,
    bot: Bot,
    base_url: str,
    path: str,
    host: str,
    port: int,
    secret: str | None,
) -> None:
    loggers.dispatcher.info("Register webhook.")
    url = f"{base_url}{path}"

    app = Application()

    await bot.set_webhook(
        url,
        allowed_updates=dp.resolve_used_update_types(),
        secret_token=secret,
    )

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=secret,
    )
    webhook_requests_handler.register(app, path=path)
    setup_application(app, dp, bot=bot)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, host=host, port=port)
    await site.start()

    await asyncio.Event().wait()
