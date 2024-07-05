"""Log out handlers."""
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.db import UnitOfWork
from bot.handlers._core import get_query_msg
from bot.keyboards import logout_board


async def logout(message: Message, i18n: I18nContext) -> None:
    """Ask confirmation to log out user from Nextcloud.

    :param message: Message object.
    :param i18n: Internationalization context.
    """
    text = i18n.get("logout")
    reply_markup = logout_board()
    await message.answer(text=text, reply_markup=reply_markup)


@get_query_msg
async def logout_confirm(
    query: CallbackQuery,
    query_msg: Message,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
    uow: UnitOfWork,
) -> None:
    """Log out the user from Nextcloud.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    :param uow: Unit of work.
    """
    await nc.ocs("DELETE", "/ocs/v2.php/core/apppassword")
    await uow.users.delete(query.from_user.id)
    await uow.commit()

    await state.clear()

    text = i18n.get("logout-confirm")
    await query_msg.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await query_msg.edit_reply_markup(None)
    await query.answer()


@get_query_msg
async def logout_cancel(query_msg: Message, i18n: I18nContext) -> None:
    """Cancel the logout operation.

    :param query: Callback query object.
    :param query_msg: Message object associated with the query.
    :param i18n: Internationalization context.
    """
    text = i18n.get("logout-cancel")
    await query_msg.edit_text(text=text, reply_markup=None)
