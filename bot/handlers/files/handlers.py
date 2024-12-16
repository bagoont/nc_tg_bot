import re
from typing import TYPE_CHECKING, Any

from aiogram import Bot, types
from aiogram_dialog import DialogManager

from bot.handlers.files import utils
from bot.states import Files

if TYPE_CHECKING:
    from nc_py_api import AsyncNextcloud, FsNode


async def on_file(callback: types.CallbackQuery, widget: Any, manager: DialogManager, item_id: str) -> None:
    nc = manager.middleware_data.get("nc")

    await utils.fetch_fsnodes_by_id(manager, nc, item_id)


async def on_back(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    fsnode: FsNode = ctx.dialog_data.get("fsnode")

    await utils.fetch_parent_fsnodes(manager, nc, fsnode)


async def on_download(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    fsnode: FsNode = ctx.dialog_data.get("fsnode")

    await utils.download_fsnode(manager, nc, fsnode)


async def on_delete(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    fsnode: FsNode = ctx.dialog_data.get("fsnode")

    await utils.delete_fsnode(manager, nc, fsnode)

    await utils.fetch_parent_fsnodes(manager, nc, fsnode)

    await manager.switch_to(Files.SCROLLGROUP)


async def on_multidownload_select(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    ctx = manager.current_context()
    ctx.dialog_data.update(checked_ids=widget.get_checked())


async def on_multidownload_confirm(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    fsnode_content: list[FsNode] = ctx.dialog_data.get("fsnode_content")
    checked_ids: list[str] = ctx.dialog_data.get("checked_ids")

    for fsnode in fsnode_content:
        if fsnode.file_id in checked_ids:
            await utils.download_fsnode(manager, nc, fsnode)

    ctx.dialog_data.pop("checked_ids")

    await callback.answer(f"Downloaded {len(checked_ids)} files.")

    await manager.switch_to(Files.SCROLLGROUP)


async def on_multidelete_select(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    ctx = manager.current_context()
    ctx.dialog_data.update(checked_ids=widget.get_checked())


async def on_multidelete_confirm(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    cur_fsnode: FsNode = ctx.dialog_data.get("fsnode")
    fsnode_content: list[FsNode] = ctx.dialog_data.get("fsnode_content")
    checked_ids: list[str] = ctx.dialog_data.get("checked_ids", [])

    for fsnode in fsnode_content:
        if fsnode.file_id in checked_ids:
            await utils.delete_fsnode(manager, nc, fsnode)

    if checked_ids:
        ctx.dialog_data.pop("checked_ids")

    await utils.fetch_fsnodes(manager, nc, cur_fsnode)

    await callback.answer(f"Deleted {len(checked_ids)} files.")

    await manager.switch_to(Files.SCROLLGROUP)


async def on_complete(message: types.Message | types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    fsnode: FsNode = ctx.dialog_data.get("fsnode")

    await utils.fetch_fsnodes(manager, nc, fsnode)

    await manager.switch_to(Files.SCROLLGROUP)


async def new_folder_handler(message: types.Message, widget: Any, manager: DialogManager) -> None:
    if message.text is None:
        # TODO: Write error message.
        raise ValueError("...")

    if not re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]?$", message.text):
        await message.answer("Folder cannot be named that way.")
        return

    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    fsnode: FsNode = ctx.dialog_data.get("fsnode")
    fsnode_content: list[FsNode] = ctx.dialog_data.get("fsnode_content")

    await utils.mkdir_fsnode(
        manager,
        nc,
        fsnode.user_path,
        message.text,
        fsnode_content,
    )

    await utils.fetch_fsnodes(manager, nc, fsnode)

    await manager.switch_to(Files.SCROLLGROUP)


async def new_file_handler(message: types.Message, widget: Any, manager: DialogManager) -> None:
    if message.document is None:
        # TODO: Write error message.
        raise ValueError("...")

    if message.document.file_name is None:
        # TODO: Write error message.
        raise ValueError("...")

    bot: Bot = manager.middleware_data.get("bot")
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    ctx = manager.current_context()
    fsnode: FsNode = ctx.dialog_data.get("fsnode")
    fsnode_content: list[FsNode] = ctx.dialog_data.get("fsnode_content")

    await utils.upload_fsnode(manager, nc, bot, fsnode, message.document.file_name, fsnode_content)

    await message.reply(f"File uploaded successfully: '{message.document.file_name}'")
