"""Authorization filter."""

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud import get_user_by_tg_id


class AuthorizedFilter(BaseFilter):
    """Filter to check if the user is authorized.

    This filter is used to verify whether the sender of a message is an authorized user.
    If the user is not authorized in Nextcloud, the bot sends a notification and blocks the
    execution of the command.
    """

    async def __call__(self, event: TelegramObject, db: AsyncSession, i18n: I18nContext) -> bool:
        """Check if the user is authorized."""
        if await get_user_by_tg_id(db, event.from_user.id):
            return True
        await event.answer(text=i18n.get("not-authorized"))
        return False
