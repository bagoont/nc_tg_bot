"""A collection of utility functions for interacting with Nextcloud files and directories using the aiogram framework.

The primary functions include uploading, downloading, and deleting files as well as listing file system nodes.
These functions are designed to be used in combination with the DialogManager provided by aiogram_dialog to create
interactive interfaces for managing files on a Nextcloud server.
"""

import io
import pathlib
from http import HTTPStatus

from aiogram import Bot, types
from aiogram_dialog import DialogManager
from nc_py_api import AsyncNextcloud, FsNode, NextcloudException

from bot.core import settings
from bot.states import Files


def _unique_name(name: str, names: list[str]) -> str:
    i = 1
    path = pathlib.Path(name)
    while name in names:
        name = f"{path.stem} ({i}){path.suffix}"
        i += 1
    return name


async def _notify(event: types.TelegramObject, text: str, *, show_alert: bool = False) -> None:
    match event:
        case types.Message():
            await event.reply(text)
        case types.CallbackQuery():
            await event.answer(text, show_alert=show_alert)
        case _:
            # TODO: Write error message.
            raise TypeError


async def _get_fsnode_by_id(
    manager: DialogManager,
    nc: AsyncNextcloud,
    file_id: int | str | FsNode,
    *,
    refresh: bool = False,
) -> FsNode | None:
    if isinstance(file_id, FsNode) and not refresh:
        return file_id

    try:
        fsnode = await nc.files.by_id(file_id)
    except NextcloudException as e:
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()

    return fsnode


async def _get_fsnode_by_path(
    manager: DialogManager,
    nc: AsyncNextcloud,
    path: str | FsNode,
    *,
    refresh: bool = False,
) -> FsNode | None:
    if isinstance(path, FsNode) and not refresh:
        return path

    try:
        fsnode = await nc.files.by_path(path)
    except NextcloudException as e:
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()

    return fsnode


async def upload_fsnode(
    manager: DialogManager,
    nc: AsyncNextcloud,
    bot: Bot,
    path: str | FsNode,
    name: str,
    fsnode_content: list[FsNode] | None = None,
    *,
    make_unique: bool = True,
) -> None:
    if not isinstance(manager.event, types.Message):
        msg = "Invalid event type. Expected a Message."
        raise TypeError(msg)

    if manager.event.document is None:
        msg = "No document provided with this message."
        raise ValueError(msg)

    if make_unique and fsnode_content is None:
        msg = (
            f"Cannot create directory '{path}/{name}' because making "
            "unique name is required for non-empty fsnode content."
        )
        raise ValueError(msg)

    if make_unique and fsnode_content is not None:
        name = _unique_name(name, [nested_fsnode.name for nested_fsnode in fsnode_content])

    file = await bot.get_file(manager.event.document.file_id)
    if file.file_path is None:
        msg = "Failed to retrieve file path."
        raise ValueError(msg)

    buff = await bot.download_file(file.file_path, chunk_size=settings.TG_CHUNK_SIZE)

    try:
        await nc.files.upload_stream(
            f"{path.user_path if isinstance(path, FsNode) else path}{name}",
            buff,
            chunk_size=settings.nc.CHUNKSIZE,
        )
    except NextcloudException as e:
        if e.status_code == HTTPStatus.NOT_FOUND:
            await manager.switch_to(Files.NOT_FOUND)
            return
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()
        return


async def mkdir_fsnode(
    manager: DialogManager,
    nc: AsyncNextcloud,
    path: str | FsNode,
    name: str,
    fsnode_content: list[FsNode] | None = None,
    *,
    make_unique: bool = True,
) -> None:
    if make_unique and fsnode_content is None:
        msg = (
            f"Cannot create directory '{path}/{name}' because making"
            " unique name is required for non-empty fsnode content."
        )
        raise ValueError(msg)

    if make_unique and fsnode_content is not None:
        name = _unique_name(name, [nested_fsnode.name for nested_fsnode in fsnode_content])

    try:
        await nc.files.mkdir(f"{path.user_path if isinstance(path, FsNode) else path}{name}")
    except NextcloudException as e:
        if e.status_code == HTTPStatus.NOT_FOUND:
            await manager.switch_to(Files.NOT_FOUND)
            return
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()
        return


async def download_fsnode(
    manager: DialogManager,
    nc: AsyncNextcloud,
    path: str | FsNode,
    *,
    refresh: bool = False,
) -> None:
    fsnode = await _get_fsnode_by_path(manager, nc, path, refresh=refresh)
    if fsnode is None:
        await manager.switch_to(Files.NOT_FOUND)
        return

    if fsnode.info.size == 0:
        # TODO: To i18n.
        await _notify(manager.event, "File cannot be empty.", show_alert=True)
        return
    if fsnode.info.size > settings.TG_UPLOAD_SIZE:
        # TODO: To i18n.
        await _notify(manager.event, "File is too big.", show_alert=True)
        return

    buff = io.BytesIO()
    try:
        await nc.files.download2stream(fsnode, buff, chunk_size=settings.nc.CHUNKSIZE)
    except NextcloudException as e:
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()
        return

    buff.seek(0)

    file = types.BufferedInputFile(buff.read(), chunk_size=settings.TG_CHUNK_SIZE, filename=fsnode.name)

    match manager.event:
        case types.CallbackQuery():
            if not isinstance(manager.event.message, types.Message):
                return

            await manager.event.message.answer_document(file)
        case types.Message():
            await manager.event.answer_document(file)
        case _:
            msg = "Document sending is not supported for this type of event."
            raise TypeError(msg)


async def delete_fsnode(
    manager: DialogManager,
    nc: AsyncNextcloud,
    path: str | FsNode,
) -> None:
    try:
        await nc.files.delete(path)
    except NextcloudException as e:
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()
        return


async def fetch_fsnodes(
    manager: DialogManager,
    nc: AsyncNextcloud,
    path: str | FsNode,
) -> None:
    try:
        fsnodes = await nc.files.listdir(path, exclude_self=False)
    except NextcloudException as e:
        if e.status_code == HTTPStatus.NOT_FOUND:
            await manager.switch_to(Files.NOT_FOUND)
            return
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()
        return

    ctx = manager.current_context()
    ctx.dialog_data.update(fsnode=fsnodes[0])
    ctx.dialog_data.update(fsnode_content=sorted(fsnodes[1:], key=lambda f: not f.is_dir))


async def fetch_fsnodes_by_id(
    manager: DialogManager,
    nc: AsyncNextcloud,
    file_id: int | str | FsNode,
) -> None:
    fsnode = await _get_fsnode_by_id(manager, nc, file_id)
    if fsnode is None:
        await manager.switch_to(Files.NOT_FOUND)
        return

    await fetch_fsnodes(manager, nc, fsnode)


async def fetch_parent_fsnodes(
    manager: DialogManager,
    nc: AsyncNextcloud,
    path: str | FsNode,
) -> None:
    if isinstance(path, FsNode):
        path = path.user_path

    path = str(pathlib.Path(path).parent)

    await fetch_fsnodes(manager, nc, path)
