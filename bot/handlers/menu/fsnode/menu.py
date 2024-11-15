"""Fsnode menu handler."""

from aiogram.types import Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers.core import get_fsnode_msg
from bot.nextcloud import RootFsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError


async def menu(message: Message, i18n: I18nContext, nc: AsyncNextcloud) -> Message:
    """Fsnode menu.

    Fsnode entry point.

    :param message: Message object.
    :param i18n: Internationalization context.
    :param nc: AsyncNextcloud.
    """
    try:
        srv = await RootFsNodeService.create_instance(nc)
    except FsNodeNotFoundError:
        return await message.reply(text=i18n.get("fsnode-not-found"))

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes)
    return await message.reply(text=text, reply_markup=reply_markup)
