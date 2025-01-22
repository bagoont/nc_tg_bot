import io
import pathlib
import re
from typing import Any, cast

from aiogram import Bot
from aiogram.types import BufferedInputFile, CallbackQuery, Document, Message
from aiogram_dialog import Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from nc_py_api import AsyncNextcloud, FsNode

from bot.core import settings
from bot.dialogs.files.states import Create, Multiselect
from bot.dialogs.files.utils import fetch_fsnodes


def _unique_name(name: str, other: list[str]) -> str:
    i = 1
    path = pathlib.Path(name)
    while name in other:
        name = f"{path.stem} ({i}){path.suffix}"
        i += 1
    return name


async def on_start(data: dict[str, Any], manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]

    if manager.start_data:
        start_data = cast(dict[str, Data], manager.start_data)
        if "path" in start_data:
            path = start_data["path"]
            del start_data["path"]
        elif "file_id" in start_data:
            path = await nc.files.by_id(start_data["file_id"])
            del start_data["file_id"]
        else:
            # TODO: Write error text.
            msg = "..."
            raise ValueError
    else:
        path = ""

    fsnodes = await fetch_fsnodes(nc, path)
    manager.dialog_data["fsnodes"] = fsnodes


async def on_subdialog_start(data: dict[str, Any], manager: DialogManager) -> None:
    start_data = cast(dict[str, Data], manager.start_data)

    manager.dialog_data["fsnodes"] = start_data["fsnodes"]
    del start_data["fsnodes"]


async def on_process_result(data: Data, result: Data, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]

    if result:
        res_data = cast(dict[str, Data], result)
        if "path" in res_data:
            path = res_data["path"]
        elif "file_id" in res_data:
            path = await nc.files.by_id(res_data["file_id"])
        else:
            msg = "Invalid result data. Please provide either 'path' or 'file_id'."
            raise ValueError(msg)
        fsnodes = await fetch_fsnodes(nc, path)
        manager.dialog_data["fsnodes"] = fsnodes


async def on_file(callback: CallbackQuery, widget: Button, manager: DialogManager, item_id: str) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]

    fsnode = await nc.files.by_id(item_id)
    fsnodes = await fetch_fsnodes(nc, fsnode)

    manager.dialog_data["fsnodes"] = fsnodes


async def on_back(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnode: FsNode = manager.dialog_data["fsnodes"][0]

    path = str(pathlib.Path(fsnode.user_path).parent)
    parent_fsnodes = await fetch_fsnodes(nc, path)

    manager.dialog_data["fsnodes"] = parent_fsnodes


async def on_download(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnode: FsNode = manager.dialog_data["fsnodes"][0]

    if fsnode.info.size == 0:
        # TODO: To i18n.
        await callback.answer(f"__zero_size__: {fsnode.name}", show_alert=True)
        return
    if fsnode.info.size > settings.TG_FILESIZE:
        # TODO: To i18n.
        await callback.answer(f"__too_big__: {fsnode.name}", show_alert=True)
        return

    buff = io.BytesIO()
    await nc.files.download2stream(fsnode, buff, chunk_size=settings.nc.CHUNKSIZE)
    buff.seek(0)
    file = BufferedInputFile(buff.read(), chunk_size=settings.TG_CHUNK_SIZE, filename=fsnode.name)

    await callback.message.answer_document(file)  # type: ignore[union-attr]


async def on_delete(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnode: FsNode = manager.dialog_data["fsnodes"][0]

    await nc.files.delete(fsnode)
    path = str(pathlib.Path(fsnode.user_path).parent)
    fsnodes = await fetch_fsnodes(nc, path)

    manager.dialog_data["fsnodes"] = fsnodes


async def on_multiselect(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    await manager.start(Multiselect.MULTISELECT, data={"fsnodes": fsnodes}, show_mode=ShowMode.EDIT)


async def on_multiselect_drop(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    manager.current_context().widget_data["multiselect"] = []


# TODO: In docs add arguments why is not backgorund.
async def on_multidownload(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    selected_ids = cast(list[str], manager.current_context().widget_data["multiselect"])

    await manager.switch_to(Multiselect.MUTLTIDOWNOLOAD, show_mode=ShowMode.EDIT)

    count = len(selected_ids)
    await manager.update({"progress": 0})
    for i, fsnode in enumerate([fsnode for fsnode in fsnodes if fsnode.file_id in selected_ids], start=1):
        if fsnode.info.size == 0:
            # TODO: Add reason with file_name.
            await callback.message.answer(f"__zero_size__: {fsnode.name}")  # type: ignore[union-attr]
            continue
        if fsnode.info.size > settings.TG_FILESIZE:
            # TODO: Add reason with file_name.
            await callback.message.answer(f"__too_big__: {fsnode.name}")  # type: ignore[union-attr]
            continue
        buff = io.BytesIO()
        await nc.files.download2stream(fsnode, buff, chunk_size=settings.nc.CHUNKSIZE)
        buff.seek(0)
        file = BufferedInputFile(buff.read(), chunk_size=settings.TG_CHUNK_SIZE, filename=fsnode.name)
        await callback.message.answer_document(file)  # type: ignore[union-attr]
        await manager.update(
            {
                "name": fsnode.name,
                "progress": i * 100 / count,
            }
        )
    await manager.done(result={"path": fsnodes[0]}, show_mode=ShowMode.SEND)


# TODO: In docs add arguments why is not backgorund.
async def on_multidelete(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    selected_ids = cast(list[str], manager.current_context().widget_data["multiselect"])

    await manager.switch_to(Multiselect.MULTIDELETE, show_mode=ShowMode.EDIT)

    count = len(selected_ids)
    await manager.update({"progress": 0})
    for i, fsnode in enumerate([fsnode for fsnode in fsnodes if fsnode.file_id in selected_ids], start=1):
        await nc.files.delete(fsnode)
        await manager.update(
            {
                "name": fsnode.name,
                "progress": i * 100 / count,
            }
        )
    await manager.done(result={"path": fsnodes[0]}, show_mode=ShowMode.SEND)


async def on_create(callback: CallbackQuery, widget: Button, manager: DialogManager) -> None:
    fsnodes = manager.dialog_data["fsnodes"]
    await manager.start(Create.TYPE, show_mode=ShowMode.SEND, data={"fsnodes": fsnodes})


async def folder_name_handler(message: Message, widget: MessageInput, manager: DialogManager) -> None:
    if not re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]?$", message.text):
        # TODO: To i18n.
        await message.answer("__invalid_folder_name__")
        return

    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]

    name = _unique_name(message.text, [node.name for node in fsnodes[1:]])
    folder = await nc.files.mkdir(f"{fsnodes[0].user_path}{name}")

    # TODO: To i18n.
    await message.reply(f"__folder_created__: {folder.name}")
    await manager.done(result={"path": fsnodes[0].user_path})


async def document_handler(message: Message, widget: MessageInput, manager: DialogManager) -> None:
    if message.document.file_name is None:
        # TODO: To i18n.
        await message.reply("__invalid_file_name__")
        return
    if message.document.file_size == 0:
        await message.reply("__invalid_file_size__")
        return
    if message.document.file_size > settings.nc.FILESIZE:
        await message.reply("__file_too_large__")
        return

    if "documents" in manager.dialog_data:
        manager.dialog_data["documents"].insert(0, message.document)
    else:
        manager.dialog_data["documents"] = [message.document]


async def on_document(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str) -> None:
    documents: list[Document] = manager.dialog_data["documents"]

    for document in documents:
        if document.file_unique_id == item_id:
            documents.remove(document)


async def clean_documents(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    if "documents" in manager.dialog_data:
        del manager.dialog_data["documents"]


# TODO: In docs add arguments why is not backgorund.
async def upload_document(callback: CallbackQuery, widget: Any, manager: DialogManager) -> None:
    bot: Bot = manager.middleware_data["bot"]
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    fsnodes: list[FsNode] = manager.dialog_data["fsnodes"]
    documents: list[Document] = manager.dialog_data["documents"]

    await manager.switch_to(Create.UPLOAD, show_mode=ShowMode.EDIT)

    count = len(documents)
    for i, document in enumerate(documents, start=1):
        file = await bot.get_file(document.file_id)
        buff = await bot.download_file(file.file_path, chunk_size=settings.TG_CHUNK_SIZE)
        name = _unique_name(document.file_name, [fsnode.name for fsnode in fsnodes[1:]])
        await nc.files.upload_stream(f"{fsnodes[0].user_path}{name}", buff, chunk_size=settings.nc.CHUNKSIZE)
        await manager.update(
            {
                "name": document.file_name,
                "progress": i * 100 / count,
            }
        )
    await manager.done(result={"path": fsnodes[0]}, show_mode=ShowMode.SEND)
