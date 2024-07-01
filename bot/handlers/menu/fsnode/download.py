from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.handlers._core import get_human_readable_bytes, get_query_msg
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import NCSrvFactory
from bot.nextcloud.exceptions import FsNodeNotFoundError


@get_query_msg
async def download(
    query: CallbackQuery,
    query_msg: Message,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> None:
    try:
        class_ = NCSrvFactory.get("FsNodeService")
        srv = await class_.create_instance(nc, file_id=callback_data.file_id)
    except FsNodeNotFoundError:
        text = i18n.get("fsnode-not-found")
        await query_msg.edit_text(text=text)
        return

    if srv.fsnode.info.size > settings.telegram.max_upload_size or srv.fsnode.info.size == 0:
        file_url = await srv.direct_download()
        text = i18n.get(
            "fsnode-url",
            size=get_human_readable_bytes(srv.fsnode.info.size),
            size_limit=get_human_readable_bytes(settings.telegram.max_upload_size),
            url=file_url,
        )
        await query_msg.answer(text=text)
        await query.answer()
        return

    await query_msg.answer_document(await srv.download())
    await query.answer()
