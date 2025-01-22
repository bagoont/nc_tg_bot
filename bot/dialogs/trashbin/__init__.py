from typing import Any

from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager, StartMode
from nc_py_api import AsyncNextcloud

from bot.dialogs.trashbin import handlers, windows
from bot.dialogs.trashbin.states import Trashbin
from bot.filters import AuthFilter
from bot.utils import Commands

router: Router = Router(name="trash_bin")


@router.message(filters.Command(Commands.trash_bin.value), AuthFilter())
async def trashbin(message: types.Message, nc: AsyncNextcloud, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(Trashbin.SCROLLGROUP, mode=StartMode.RESET_STACK)


dialog = Dialog(
    windows.scrollgroup(),
    windows.trash_item(),
    windows.cleanup(),
    name="trash_bin",
    on_start=handlers.on_start,
)

router.include_router(dialog)
