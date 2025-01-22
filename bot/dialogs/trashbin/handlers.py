from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from nc_py_api import AsyncNextcloud, FsNode

from bot.dialogs.trashbin.states import Trashbin


async def on_start(data: dict[str, Any], dialog_manager: DialogManager) -> None:
    nc: AsyncNextcloud = dialog_manager.middleware_data.get("nc")
    dialog_manager.dialog_data["trashbin"] = await nc.files.trashbin_list()


async def on_trash(callback: types.CallbackQuery, widget: Any, manager: DialogManager, item_id: str) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]

    trash_item = await nc.files.by_id(item_id)

    manager.dialog_data["trash_item"] = trash_item
    await manager.switch_to(Trashbin.TRASH)


async def on_delete(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    trash_item: FsNode = manager.dialog_data["trash_item"]

    await nc.files.trashbin_delete(trash_item)

    manager.dialog_data["trashbin"] = await nc.files.trashbin_list()
    del trash_item
    await manager.switch_to(Trashbin.SCROLLGROUP)


async def on_restore(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]
    trash_item: FsNode = manager.dialog_data["trash_item"]

    await nc.files.trashbin_restore(trash_item)

    manager.dialog_data["trashbin"] = await nc.files.trashbin_list()
    del trash_item
    await manager.switch_to(Trashbin.SCROLLGROUP)


async def on_cleanup(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data["nc"]

    await nc.files.trashbin_cleanup()

    await manager.switch_to(Trashbin.EMPTY)
