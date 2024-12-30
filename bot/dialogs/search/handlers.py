from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from nc_py_api import AsyncNextcloud, NextcloudException

from bot.dialogs.files.states import Files
from bot.states import Search

DD_FSNODES_KEY = "fsnodes"


async def search_query_handler(message: types.Message, widget: Any, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    try:
        fsnodes = await nc.files.find(["like", "name", f"%{message.text}%"])
    except NextcloudException as e:
        await message.reply(e.reason, show_alert=True)
        await manager.done()
        return

    ctx = manager.current_context()
    ctx.dialog_data[DD_FSNODES_KEY] = fsnodes

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
