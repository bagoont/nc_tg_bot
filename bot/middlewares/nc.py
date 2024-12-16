"""Async Nextcloud client middleware."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.db import UserRepository


class NextcloudMD(BaseMiddleware):
    """Middleware for Nextcloud.

    Injects :class:`AsyncNextcloud` instance into the handler context.

    :param handler: The handler function to be executed.
    :param event: The event object.
    :param data: The data dictionary containing the request context.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Calls the handler function with the injected Nextcloud instance."""
        users: UserRepository | None = data.get("users")
        if users is None:
            msg = "'AsyncSession' object not found."
            raise ValueError(msg)

        user = await users.get_by_tg_id(event.from_user.id)
        url = f"{settings.nc.SCHEME}://{settings.nc.HOST}:{settings.nc.PORT}"
        data["nc"] = AsyncNextcloud(
            nextcloud_url=url,
            nc_auth_user=user.login if user else None,
            nc_auth_pass=user.app_password if user else None,
        )
        return await handler(event, data)
