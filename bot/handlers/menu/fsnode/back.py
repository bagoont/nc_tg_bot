"""Handler for moving to the parent directory."""
from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers._core import get_fsnode_msg, get_query_msg
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError


@get_query_msg
async def back(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    """Move to the parent directory.

    :param query: Callback query object.
    :param query_msg: The message object associated with the query.
    :param callback_data: The callback data object containing the necessary data for the action with fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    try:
        class_ = NCSrvFactory.get("PrevFsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes, query.from_user.id)
    with suppress(TelegramBadRequest):
        await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer()