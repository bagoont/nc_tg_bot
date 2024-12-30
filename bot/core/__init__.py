"""Core functionalities of the Nextcloud Telegram Bot."""

from bot.core.config import SQLITE_URL, settings
from bot.core.loaders import _storage, bot, dp
from bot.core.runners import on_shutdown, on_startup, webhook_run

__all__ = ("settings", "SQLITE_URL", "bot", "dp", "_storage", "on_startup", "on_shutdown", "webhook_run")
