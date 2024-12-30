"""Authorization filter."""

from aiogram import filters, types

from bot.db import UserRepository


class AuthFilter(filters.BaseFilter):
    """Filter to check if the user is authorized.

    This filter is used to verify whether the sender of a message is an authorized user.
    If the user is not authorized in Nextcloud, the bot sends a notification and blocks the
    execution of the command.
    """

    async def __call__(self, event: types.Message, users: UserRepository) -> bool:
        """Check if the user is authorized."""
        if event.from_user is None:
            raise ValueError

        if await users.get_by_tg_id(event.from_user.id):
            return True
        await event.answer("PROHIBIT")
        return False
