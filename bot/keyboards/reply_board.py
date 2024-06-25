from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import KeyboardButton


def reply_board(
    *texts: LazyProxy,
    is_persistent: bool | None = None,
    resize_keyboard: bool | None = None,
    one_time_keyboard: bool | None = None,
    selective: bool | None = None,
    input_field_placeholder: str | None = None,
    row_width: int = 2,
) -> ReplyKeyboardMarkup:
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=text) for text in texts], width=row_width)
    return builder.as_markup(
        is_persistent=is_persistent,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )
