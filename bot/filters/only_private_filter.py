"""Authorization filter."""

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext


class OnlyPrivateFilter(BaseFilter):
    """Filter to check if the event is a message in a private chat."""

    async def __call__(self, event: TelegramObject, i18n: I18nContext) -> bool:
        """Check chat is private."""
        if event.chat.type != "private":
            await event.answer(text=i18n.get("only-private"))
            return False
        return True
