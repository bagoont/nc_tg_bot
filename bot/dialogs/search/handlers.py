from typing import Any, cast

from aiogram import types
from aiogram_dialog import Data, DialogManager
from nc_py_api import AsyncNextcloud

from bot.dialogs.files.states import Files
from bot.dialogs.search.states import Search


async def on_start(data: dict[str, Any], manager: DialogManager) -> None:
    if manager.start_data:
        start_data = cast(dict[str, Data], manager.start_data)
        nc: AsyncNextcloud = manager.middleware_data.get("nc")

        fsnodes = await nc.files.find(["like", "name", f"%{start_data['query']}%"])

        manager.dialog_data["fsnodes"] = fsnodes


async def search_query_handler(message: types.Message, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    fsnodes = await nc.files.find(["like", "name", f"%{message.text}%"])

    ctx = manager.current_context()
    ctx.dialog_data["fsnodes"] = fsnodes

    if not fsnodes:
        await manager.switch_to(Search.NOT_FOUND)
        return
    await manager.switch_to(Search.SCROLLGROUP)


async def on_file(
    message: types.Message,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    await manager.done()

    await manager.start(Files.SCROLLGROUP, data={"file_id": item_id})
