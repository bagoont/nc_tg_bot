"""Unit of work midlleware."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.db import UnitOfWork


class UnitOfWorkMD(BaseMiddleware):
    """A middleware that creates and manages Unit of work session for the duration of the request.

    Injects :class:`UnitOfWork` instance into the handler context.

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
        """Executes the handler within a database session."""
        session_maker = data.get("_session_maker")
        if session_maker is None:
            msg = "async_sessionmaker object not found."
            raise ValueError(msg)
        async with UnitOfWork(session_maker) as uow:
            data["uow"] = uow
            return await handler(event, data)
