from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager
from nc_py_api import AsyncNextcloud

from . import windows
from bot.db import session_maker
from bot.filters import AuthFilter
from bot.middlewares import DatabaseMD, NextcloudMD
from bot.states import Settings
from bot.utils import Commands

router = Router(name="files")

router.message.outer_middleware.register(DatabaseMD(session_maker))
router.message.middleware.register(NextcloudMD())
router.callback_query.outer_middleware.register(DatabaseMD(session_maker))
router.callback_query.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.settings.value), AuthFilter())
async def files(message: types.Message, nc: AsyncNextcloud, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(Settings.MAIN)


dialog = Dialog(
    windows.main_window(),
    windows.lang_window(),
    windows.logout_window(),
)

router.include_router(dialog)
