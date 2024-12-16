"""Authorization filter."""

from aiogram import filters, types


class ChatTypeFilter(filters.BaseFilter):
    """Filter to check if the event is a message in a private chat."""

    def __init__(self, chat_type: str | list[str]):
        self.chat_type = chat_type

    async def __call__(self, event: types.Message) -> bool:
        if isinstance(self.chat_type, str):
            return event.chat.type == self.chat_type
        return event.chat.type in self.chat_type
