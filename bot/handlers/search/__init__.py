from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager
from nc_py_api import AsyncNextcloud

from . import windows
from . import utils
from bot.db import session_maker
from bot.filters import AuthFilter
from bot.middlewares import DatabaseMD, NextcloudMD
from bot.states import Search
from bot.utils import Commands

router = Router(name="search")

router.message.outer_middleware.register(DatabaseMD(session_maker))
router.message.middleware.register(NextcloudMD())
router.callback_query.outer_middleware.register(DatabaseMD(session_maker))
router.callback_query.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.search.value), AuthFilter())
async def search(
    message: types.Message,
    command: filters.CommandObject,
    nc: AsyncNextcloud,
    dialog_manager: DialogManager,
) -> None:
    if command.args:
        await dialog_manager.start(Search.SCROLLGROUP, data={"query": command.args})
        return

    await dialog_manager.start(Search.INPUT_QUERY)


async def on_start(data: dict, dialog_manager: DialogManager) -> None:
    nc: AsyncNextcloud = dialog_manager.middleware_data.get("nc")

    if dialog_manager.start_data:
        match dialog_manager.start_data:
            case {"query": query}:
                await utils.search_fsnodes(dialog_manager, nc, ["like", "name", f"%{query}%"])
            case _:
                # TODO: Write error.
                raise ValueError


dialog = Dialog(
    windows.input_query_window(),
    windows.search_result_window(),
    windows.not_found_window(),
    on_start=on_start,
)

router.include_router(dialog)
