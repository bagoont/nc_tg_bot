from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager

from bot.states import Trash_bin

DD_CHECKED_IDS_KEY = "checked_ids"


async def on_trash(callback: types.CallbackQuery, widget: Any, manager: DialogManager, item_id: str) -> None:
    print(item_id)

    await manager.switch_to(Trash_bin.TRASH)


async def on_delete(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    print("delete")


async def on_restore(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    print("restore")


async def on_cleanup(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    print("cleanup")


async def on_multidelete(
    callback: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    ctx = manager.current_context()
    ctx.dialog_data[DD_CHECKED_IDS_KEY] = widget.get_checked()


async def on_multidelete_confirm(callback: types.CallbackQuery, widget: Any, manager: DialogManager) -> None:
    ctx = manager.current_context()
    checked_ids = ctx.dialog_data[DD_CHECKED_IDS_KEY]
    print(checked_ids)
