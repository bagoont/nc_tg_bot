"""Async Nextcloud client middleware."""

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from nc_py_api import AsyncNextcloud

from bot.core import settings

if TYPE_CHECKING:
    from bot.db import UnitOfWork


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
        uow: UnitOfWork | None = data.get("uow")
        if uow is None:
            msg = "'UnitOfWork' object not found."
            raise ValueError(msg)
        if not hasattr(event, "from_user"):
            msg = "Telegram event object must have 'from_user' attribute."
            raise AttributeError(msg)
        user = await uow.users.get_by_id(event.from_user.id)
        url = f"{settings.nc.SCHEME}://{settings.nc.HOST}:{settings.nc.PORT}"
        data["nc"] = AsyncNextcloud(
            nextcloud_url=url,
            nc_auth_user=user.nc_login if user else None,
            nc_auth_pass=user.nc_app_password if user else None,
        )
        return await handler(event, data)
