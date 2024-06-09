from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from nc_py_api import AsyncNextcloud

from bot.core import settings

if TYPE_CHECKING:
    from bot.db import UnitOfWork


class NextcloudMD(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        db: UnitOfWork | None = data.get("db")
        if db is None:
            msg = "'UnitOfWork' object not found."
            raise RuntimeError(msg)
        user = await db.users.get_by_id(event.from_user.id)
        data["nc"] = AsyncNextcloud(
            nextcloud_url=settings.nextcloud.url,
            nc_auth_user=user.nc_login if user else None,
            nc_auth_pass=user.nc_app_password if user else None,
        )
        return await handler(event, data)
