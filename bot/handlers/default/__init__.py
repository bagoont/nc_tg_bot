"""Router with default messages."""

from aiogram import Router
from aiogram.filters.command import Command

from .default import help_msg, start


def default_router() -> Router:
    """Build router with default messages.

    :return: Router with default messages.
    """
    router = Router()

    router.message.register(start, Command("start"))
    router.message.register(help_msg, Command("help"))

    return router
