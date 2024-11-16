"""Handler with pagination for trash bin."""

from typing import cast

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers.core import get_trashbin_msg
from bot.keyboards.callback_data_factories import TrashbinActions, TrashbinData
from bot.nextcloud import TrashbinService


async def pag(
    query: CallbackQuery,
    i18n: I18nContext,
    callback_data: TrashbinData,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Pagination for trash bin.

    :param query: Callback query object.
    :param callback_data: Callback data object containing the necessary data for the search result.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    query_msg = cast(Message, query.message)

    page_num = int(callback_data.page)
    page = page_num + 1 if callback_data.action == TrashbinActions.PAG_NEXT else page_num - 1

    srv = await TrashbinService.create_instance(nc)

    text, reply_markup = get_trashbin_msg(i18n, srv.trashbin, srv.get_size(), page=page)
    return await query_msg.edit_text(text=text, reply_markup=reply_markup)
