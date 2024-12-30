from http import HTTPStatus
from typing import Any

from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager
from nc_py_api import AsyncNextcloud, FsNode, NextcloudException

from bot.dialogs.search import windows
from bot.filters import AuthFilter
from bot.states import Search
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


async def process_start_data(data: dict[str, Any], nc: AsyncNextcloud) -> str | FsNode:
    if data.get(SD_QUERY_KEY):
        return data[SD_QUERY_KEY]
    msg = "Invalid start data. Please provide either 'path' or 'file_id'."
    raise ValueError(msg)


async def on_start(data: dict[str, Any], dialog_manager: DialogManager) -> None:
    if dialog_manager.start_data:
        if not isinstance(dialog_manager.start_data, dict):
            msg = "..."
            raise TypeError(msg)

        nc: AsyncNextcloud = dialog_manager.middleware_data.get(NEXTCLOUD_KEY)

        try:
            query = await process_start_data(dialog_manager.start_data, nc)
            fsnodes = await nc.files.find(query, ["like", "name", f"%{query}%"])
        except NextcloudException as e:
            if e.status_code == HTTPStatus.NOT_FOUND:
                await dialog_manager.switch_to(Search.NOT_FOUND)
                return
            if isinstance(dialog_manager.event, types.Message):
                await dialog_manager.event.reply(e.reason)
            if isinstance(dialog_manager.event, types.CallbackQuery):
                await dialog_manager.event.answer(e.reason, show_alert=True)
            await dialog_manager.done()
            return


dialog = Dialog(
    windows.input_window(),
    windows.scrollgroup_window(),
    windows.not_found_window(),
    on_start=on_start,
    name="search",
)

router.include_router(dialog)
