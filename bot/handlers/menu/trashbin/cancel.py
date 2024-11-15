"""Cancel operation with trash bin handler."""

from typing import cast

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers.core import get_trashbin_msg
from bot.keyboards.callback_data_factories import TrashbinData
from bot.nextcloud import TrashbinService


async def cancel_callback(
    query: CallbackQuery,
    callback_data: TrashbinData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Cancel operation with trash bin.

    :param query: Callback query object.
    :param callback_data: Callback data object containing the necessary data for the trash bin.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    query_msg = cast(Message, query.message)

    srv = await TrashbinService.create_instance(nc)

    text, reply_markup = get_trashbin_msg(
        i18n,
        srv.trashbin,
        srv.get_size(),
        page=callback_data.page,
    )
    return await query_msg.edit_text(text=text, reply_markup=reply_markup)
