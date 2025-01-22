from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager
from nc_py_api import AsyncNextcloud

from bot.dialogs.settings import windows
from bot.dialogs.settings.states import Settings
from bot.filters import AuthFilter
from bot.utils import Commands

router: Router = Router(name="files")


@router.message(filters.Command(Commands.settings.value), AuthFilter())
async def files(message: types.Message, nc: AsyncNextcloud, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(Settings.MAIN)


dialog = Dialog(
    windows.main_window(),
    windows.lang_window(),
    windows.logout_window(),
    name="settings",
)

router.include_router(dialog)
