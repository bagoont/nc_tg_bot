"""Functions to handle bot startup, shutdown, and webhook operations."""

import asyncio

from aiogram import Bot, Dispatcher, loggers
from aiogram.enums import MenuButtonType
from aiogram.types import BotCommand, MenuButtonWebApp, WebAppInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from aiohttp.web import Application, AppRunner, TCPSite

from bot.core.config import settings
from bot.handlers import routers
from bot.middlewares import LocaleManager, QueryMsgMD


async def set_menu_button(bot: Bot) -> None:
    """Set menu button in Telegram if base url of Nextclout use secure scheme."""
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
    """Set avliable commands in Telegram."""
    await set_menu_button(bot)

    commands = [
        BotCommand(command="help", description="Get message with help text"),
        BotCommand(command="auth", description="Start authentification in Nextcloud"),
        BotCommand(command="logout", description="Logout from Nextcloud"),
    ]

    await bot.set_my_commands(commands)


async def on_startup(dispatcher: Dispatcher, bot: Bot) -> None:
    """Initializes the bot by setting up handlers, middleware, and registering bot commands.

    :param dispatcher: Aiogram dispatcher instance.
    :param bot: Aiogram bot instance.
    """
    loggers.dispatcher.info("Bot starting...")

    await set_bot_menu(bot)

    for router in routers:
        dispatcher.include_router(router())

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="./bot/locales/{locale}/"),
        manager=LocaleManager(),
    )
    i18n_middleware.setup(dispatcher=dispatcher)
    dispatcher.callback_query.middleware.register(QueryMsgMD())

    loggers.dispatcher.info("Bot started.")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    """Performs necessary cleanup when the bot is shutting down.

    :param dispatcher: Aiogram dispatcher instance.
    :param bot: Aiogram bot instance.
    """
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
    """Sets up and starts the webhook server for receiving updates via HTTP requests.

    :param dispatcher: Aiogram dispatcher instance.
    :param bot: Aiogram bot instance.
    :param path: The path under which the webhook endpoint is accessible.
    :param host: The hostname where the webhook should be hosted
    :param port: The port number on which the webhook server listens.
    :param secret: A secret token used for webhook verification, defaults to None.
    """
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
