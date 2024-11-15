"""Fsnode delete handlers."""

from contextlib import suppress
from typing import cast

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers.core import get_fsnode_msg
from bot.keyboards import fsnode_delete_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import FsNodeService, PrevFsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError


async def delete(
    query: CallbackQuery,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Ask confirmation to delete fsnode.

    :param query: Callback query object.
    :param callback_data: Callback data object containing the necessary data for fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    query_msg = cast(Message, query.message)

    try:
        srv = await FsNodeService.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        return await query_msg.edit_text(text=i18n.get("fsnode-not-found"))

    reply_markup = fsnode_delete_board(fsnode=srv.fsnode, page=callback_data.page)
    return await query_msg.edit_text(
        text=i18n.get("fsnode-delete", name=srv.fsnode.name),
        reply_markup=reply_markup,
    )


async def delete_confirm(
    query: CallbackQuery,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Delete fsnode.

    :param query: Callback query object.
    :param callback_data: Callback data object containing the necessary data for fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    query_msg = cast(Message, query.message)

    try:
        srv = await FsNodeService.create_instance(nc, file_id=callback_data.file_id)
        prev_srv = await PrevFsNodeService.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        return await query_msg.edit_text(text=i18n.get("fsnode-not-found"))

    await srv.delete()
    prev_srv.attached_fsnodes.remove(srv.fsnode)

    text, reply_markup = get_fsnode_msg(
        i18n,
        prev_srv.fsnode,
        prev_srv.attached_fsnodes,
        page=callback_data.page,
    )
    with suppress(TelegramBadRequest):
        msg = await query_msg.edit_text(text=text, reply_markup=reply_markup)

    await query.answer(text=i18n.get("fsnode-delete-alert"), show_alert=True)

    return msg
