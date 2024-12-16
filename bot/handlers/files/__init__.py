from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager, LaunchMode
from nc_py_api import AsyncNextcloud

from . import utils, windows
from bot.db import session_maker
from bot.filters import AuthFilter
from bot.middlewares import DatabaseMD, NextcloudMD
from bot.states import Files
from bot.utils import Commands

router = Router(name="files")

router.message.outer_middleware.register(DatabaseMD(session_maker))
router.message.middleware.register(NextcloudMD())
router.callback_query.outer_middleware.register(DatabaseMD(session_maker))
router.callback_query.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.files.value), AuthFilter())
async def files(
    message: types.Message,
    command: filters.CommandObject,
    nc: AsyncNextcloud,
    dialog_manager: DialogManager,
) -> None:
    if command.args:
        await dialog_manager.start(Files.SCROLLGROUP, data={"path": command.args})
        return

    await dialog_manager.start(Files.SCROLLGROUP)


async def on_start(data: dict, dialog_manager: DialogManager) -> None:
    nc: AsyncNextcloud = dialog_manager.middleware_data.get("nc")

    if dialog_manager.start_data:
        match dialog_manager.start_data:
            case {"path": path}:
                await utils.fetch_fsnodes(dialog_manager, nc, path)
            case {"file_id": file_id}:
                await utils.fetch_fsnodes_by_id(dialog_manager, nc, file_id)
            case _:
                msg = "Invalid start data. Please provide either 'path' or 'file_id'."
                raise ValueError(msg)
    else:
        await utils.fetch_fsnodes(dialog_manager, nc, "")


dialog = Dialog(
    windows.scrollgroup_window(),
    windows.multidownload_window(),
    windows.multidelete_window(),
    windows.new_window(),
    windows.new_folder_window(),
    windows.new_file_window(),
    windows.not_found_window(),
    on_start=on_start,
    launch_mode=LaunchMode.SINGLE_TOP,
)

router.include_router(dialog)
