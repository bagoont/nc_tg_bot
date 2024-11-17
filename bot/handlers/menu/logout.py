"""Log out handlers."""

from typing import cast

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import logout_board
from bot.db.crud import get_user_by_tg_id, delete_user


async def logout(message: Message, i18n: I18nContext) -> Message:
    """Ask confirmation to log out user from Nextcloud.

    :param message: Message object.
    :param i18n: Internationalization context.
    """
    return await message.answer(text=i18n.get("logout"), reply_markup=logout_board())


async def logout_confirm(
    query: CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
    db: AsyncSession,
) -> Message:
    """Log out the user from Nextcloud.

    :param query: Callback query object.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    :param uow: Unit of work.
    """
    query_msg = cast(Message, query.message)

    await nc.ocs("DELETE", "/ocs/v2.php/core/apppassword")

    user = await get_user_by_tg_id(db, query.from_user.id)
    await delete_user(db, user.id)

    await state.clear()

    await query_msg.edit_reply_markup(None)

    return await query_msg.answer(
        text=i18n.get("logout-confirm"),
        reply_markup=ReplyKeyboardRemove(),
    )


async def logout_cancel(query: CallbackQuery, i18n: I18nContext) -> Message | bool:
    """Cancel the logout operation.

    :param query: Callback query object.
    :param i18n: Internationalization context.
    """
    query_msg = cast(Message, query.message)

    return await query_msg.edit_text(text=i18n.get("logout-cancel"), reply_markup=None)
