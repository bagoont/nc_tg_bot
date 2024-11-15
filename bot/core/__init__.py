"""Core functionalities of the Nextcloud Telegram Bot."""

from .config import settings, SQLITE_URL
from .loaders import _storage, bot, dp
from .runners import on_shutdown, on_startup, webhook_run

__all__ = (
    "settings",
    "SQLITE_URL",
    "bot",
    "dp",
    "_storage",
    "on_startup",
    "on_shutdown",
    "webhook_run",
)
