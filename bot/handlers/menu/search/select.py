"""Selection of a search result handler."""

from typing import cast

from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers.core import get_fsnode_msg
from bot.keyboards.callback_data_factories import SearchFsNodeData
from bot.nextcloud import FsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError


async def select(
    query: CallbackQuery,
    callback_data: SearchFsNodeData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message:
    """Selection of a search result.

    Send the menu of the selected fsnode.

    :param query: Callback query object.
    :param callback_data: Callback data object containing the necessary data for the search result.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    query_msg = cast(Message, query.message)

    try:
        srv = await FsNodeService.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        return await query_msg.answer(text=i18n.get("fsnode-not-found"))

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes)
    msg = await query_msg.answer(text=text, reply_markup=reply_markup)

    await query.answer()

    return msg
