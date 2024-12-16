from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from nc_py_api import AsyncNextcloud

from bot.states import Files, Search


async def search_query_handler(message: types.Message, widget: MessageInput, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    fsnodes = await nc.files.find(["like", "name", f"%{message.text}%"])

    ctx = manager.current_context()
    ctx.dialog_data.update(fsnodes=fsnodes)

    if not fsnodes:
        await manager.switch_to(Search.NOT_FOUND)
        return

    await manager.switch_to(Search.SCROLLGROUP)


async def on_file(
    message: types.Message,
    widget: MessageInput,
    manager: DialogManager,
    item_id: str,
) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    fsnode = await nc.files.by_id(item_id)
    fsnodes = await nc.files.listdir(fsnode, exclude_self=False)

    await manager.done()

    await manager.start(Files.SCROLLGROUP, data={"fsnodes": fsnodes})
