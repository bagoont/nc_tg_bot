from typing import Any

from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager
from nc_py_api import AsyncNextcloud

from bot.dialogs.trash_bin import windows
from bot.filters import AuthFilter
from bot.utils import Commands

router: Router = Router(name="trash_bin")


@router.message(filters.Command(Commands.trash_bin.value), AuthFilter())
async def trashbin(message: types.Message, nc: AsyncNextcloud, dialog_manager: DialogManager) -> None:
    await message.answer("trash_bin")


async def on_start(data: dict[str, Any], dialog_manager: DialogManager) -> None:
    nc: AsyncNextcloud = dialog_manager.middleware_data.get("nc")

    # await fetch_trash_bin(dialog_manager, nc)


dialog = Dialog(
    windows.scrollgroup_window(),
    windows.multidelete_window(),
    windows.trash_window(),
    windows.cleanup_window(),
    name="trash_bin",
    on_start=on_start,
)

router.include_router(dialog)
