"""Logout keyboard."""

from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.callback_data_factories import LogoutActions, LogoutData


def logout_board() -> InlineKeyboardMarkup:
    """Create logout keyboard.

    :return: InlineKeyboardMarkup object.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("confirm-button"),
                    callback_data=LogoutData(action=LogoutActions.CONFIRM).pack(),
                ),
                InlineKeyboardButton(
                    text=LazyProxy("deny-button"),
                    callback_data=LogoutData(action=LogoutActions.DENY).pack(),
                ),
            ],
        ],
    )
