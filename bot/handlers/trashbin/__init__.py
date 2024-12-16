from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager
from nc_py_api import AsyncNextcloud

from bot.db import session_maker
from bot.filters import AuthFilter
from bot.middlewares import DatabaseMD, NextcloudMD
from bot.utils import Commands

router = Router(name="trashbin")

router.message.outer_middleware.register(DatabaseMD(session_maker))
router.message.middleware.register(NextcloudMD())
router.callback_query.outer_middleware.register(DatabaseMD(session_maker))
router.callback_query.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.trashbin.value), AuthFilter())
async def trashbin(message: types.Message, nc: AsyncNextcloud, dialog_manager: DialogManager) -> None:
    await message.answer("trashbin")


# dialog = Dialog()

# router.include_router(dialog)
