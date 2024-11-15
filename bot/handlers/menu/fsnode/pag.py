"""Handler with pagination for fsnode menu."""

from contextlib import suppress
from typing import cast

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers.core import get_fsnode_msg
from bot.keyboards.callback_data_factories import FsNodeMenuActions, FsNodeMenuData
from bot.nextcloud import FsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError


async def pag(
    query: CallbackQuery,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Pagination for fsnode menu.

    :param query: Callback query object.
    :param callback_data: Callback data object containing the necessary data for fsnode.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    query_msg = cast(Message, query.message)

    try:
        srv = await FsNodeService.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        return await query_msg.edit_text(text=i18n.get("fsnode-not-found"))

    page_num = int(callback_data.page)
    page = page_num + 1 if callback_data.action == FsNodeMenuActions.PAG_NEXT else page_num - 1

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, page=page)
    with suppress(TelegramBadRequest):
        msg = await query_msg.edit_text(text=text, reply_markup=reply_markup)
    return msg
