from typing import Any, cast

from aiogram import Router, filters, types
from aiogram_dialog import Data, Dialog, DialogManager
from nc_py_api import AsyncNextcloud, FsNode, NextcloudException

from bot.dialogs.search import handlers, windows
from bot.dialogs.search.states import Search
from bot.filters import AuthFilter
from bot.utils import Commands

router: Router = Router(name="search")

SD_QUERY_KEY = "query"


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


dialog = Dialog(
    windows.input_query(),
    windows.scrollgroup(),
    windows.not_found(),
    on_start=handlers.on_start,
    name="search",
)

router.include_router(dialog)
