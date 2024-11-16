"""File or directory creation handlers."""

from typing import cast

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Document, Message
from aiogram_i18n import I18nContext, LazyProxy
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.handlers.core import get_fsnode_msg, get_human_readable_bytes
from bot.keyboards import fsnode_new_board, menu_board, reply_board
from bot.keyboards.callback_data_factories import FsNodeMenuData
from bot.nextcloud import FsNodeService
from bot.nextcloud.exceptions import FsNodeNotFoundError
from bot.states import FsNodeMenuStatesGroup


async def new(
    query: CallbackQuery,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message | bool:
    """Creating a new file or directory menu.

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

    reply_markup = fsnode_new_board(fsnode=srv.fsnode, page=callback_data.page)
    return await query_msg.edit_text(
        text=i18n.get("fsnode-new", name=srv.fsnode.name),
        reply_markup=reply_markup,
    )


async def upload_start(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
) -> Message:
    """Initiate file upload to Nextcloud process.

    :param query: Callback query object.
    :param state: State machine context.
    :param callback_data: Callback data object containing the necessary data for fsnode.
    :param i18n: I18nContext.
    :param nc: AsyncNextcloud.
    """
    query_msg = cast(Message, query.message)

    await state.set_state(FsNodeMenuStatesGroup.UPLOAD)
    await state.update_data(file_id=callback_data.file_id)

    reply_markup = reply_board(
        LazyProxy("stop-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    msg = await query_msg.answer(
        text=i18n.get("fsnode-upload-start", username=query.from_user.username),
        reply_markup=reply_markup,
    )
    await query.answer()

    return msg


async def upload(  # noqa: PLR0911
    message: Message,
    bot: Bot,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message:
    """Upload a file to the Nextcloud server.

    Set state to UPLOAD status and start waiting message with pinned documents to upload to
    Nextcloud or cancelation.

    :param message: Message object.
    :param bot: Bot object.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: AsyncNextcloud.
    """
    msg_doc = cast(Document, message.document)
    if msg_doc.file_name is None:
        return await message.reply(text=i18n.get("fsnode-upload-error"))

    data = await state.get_data()

    try:
        srv = await FsNodeService.create_instance(nc, file_id=data["file_id"])
    except FsNodeNotFoundError:
        return await message.reply(text=i18n.get("fsnode-not-found"))

    if msg_doc.file_size is None or msg_doc.file_size == 0:
        return await message.answer(text=i18n.get("fsnode-empty"))

    if msg_doc.file_size > settings.nc.FILESIZE:
        return await message.answer(
            text=i18n.get(
                "fsnode-size-limit",
                size=get_human_readable_bytes(msg_doc.file_size),
                size_limit=get_human_readable_bytes(settings.nc.FILESIZE),
            ),
        )

    tg_file_obj = await bot.get_file(msg_doc.file_id)
    if tg_file_obj.file_path is None:
        return await message.reply(text=i18n.get("fsnode-upload-error"))

    try:
        buff = await bot.download_file(tg_file_obj.file_path, chunk_size=settings.nc.CHUNKSIZE)
    except TelegramBadRequest:
        return await message.reply(text=i18n.get("fsnode-upload-error"))

    if buff is None:
        return await message.reply(text=i18n.get("fsnode-upload-error"))

    await srv.upload(buff, msg_doc.file_name)

    return await message.reply(text=i18n.get("fsnode-upload-success", name=msg_doc.file_name))


async def mkdir_start(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: FsNodeMenuData,
    i18n: I18nContext,
) -> Message:
    """Initiate creation of a new directory on Netxcloud server.

    Set state to MKDIR status and start waiting message with name for new directory or cancelation.

    :param query: Callback query object.
    :param state: State machine context.
    :param callback_data: Callback data object containing the necessary data for fsnode.
    :param i18n: I18nContext.
    """
    query_msg = cast(Message, query.message)

    await state.set_state(FsNodeMenuStatesGroup.MKDIR)
    await state.update_data(file_id=callback_data.file_id)

    reply_markup = reply_board(
        LazyProxy("cancel-button"),
        is_persistent=True,
        resize_keyboard=True,
        selective=True,
    )
    msg = await query_msg.answer(
        text=i18n.get("fsnode-mkdir-start", username=query.from_user.username),
        reply_markup=reply_markup,
    )
    await query.answer()

    return msg


async def mkdir(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message:
    """Create a new directory on Nextcloud server.

    End process after creation.

    :param message: Message object.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: AsyncNextcloud.
    """
    msg_text = cast(str, message.text)

    data = await state.get_data()

    try:
        srv = await FsNodeService.create_instance(nc, file_id=data["file_id"])
    except FsNodeNotFoundError:
        return await message.reply(text=i18n.get("fsnode-not-found"))

    new_dir = await srv.mkdir(msg_text)

    menu_reply_markup = menu_board()
    menu_text = i18n.get("fsnode-mkdir-success", name=new_dir.name)
    await message.reply(text=menu_text, reply_markup=menu_reply_markup)

    await state.clear()

    text, reply_markup = get_fsnode_msg(i18n, srv.fsnode, srv.attached_fsnodes)
    return await message.reply(text=text, reply_markup=reply_markup)


async def upload_incorrectly(message: Message, i18n: I18nContext) -> Message:
    """File for uploading to the server is incorrectly.

    :param message: Message object.
    :param i18n: Internationalization context.
    """
    return await message.reply(text=i18n.get("fsnode-upload-incorrectly"))


async def incorrectly_mkdir(message: Message, i18n: I18nContext) -> Message:
    """Name for directory is incorrectly.

    :param message: Message object.
    :param i18n: Internationalization context.
    """
    return await message.reply(text=i18n.get("fsnode-mkdir-incorrectly"))
