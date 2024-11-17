from collections.abc import Awaitable, Callable
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DatabaseMD(BaseMiddleware):
    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.session() as session:
            data["session"] = session
            return await handler(event, data)
