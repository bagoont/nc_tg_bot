"""Download fsnode handler."""

from typing import cast

from aiogram.types import CallbackQuery, Document, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.handlers.core import get_human_readable_bytes
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import FsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError


async def download(
    query: CallbackQuery,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | Document | bool:
    """Downloads a file from Nextcloud server.

    If the file is larger than the specified size, then a link will be sent,
    which will be valid for 8 hours.

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

    if srv.fsnode.info.size == 0:
        return await query.answer(text=i18n.get("fsnode-empty"))

    if srv.fsnode.info.size > settings.TG_UPLOAD_SIZE:
        text = i18n.get(
            "fsnode-size-limit",
            size=get_human_readable_bytes(srv.fsnode.info.size),
            size_limit=get_human_readable_bytes(settings.TG_UPLOAD_SIZE),
        )
        return await query.answer(text=text)

    doc = await query_msg.answer_document(await srv.download())
    await query.answer()

    return doc
