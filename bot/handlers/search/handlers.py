from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from nc_py_api import AsyncNextcloud

from bot.handlers.search import utils
from bot.states import Files, Search


async def search_query_handler(message: types.Message, widget: MessageInput, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")

    await utils.search_fsnodes(manager, nc, ["like", "name", f"%{message.text}%"])

    await manager.switch_to(Search.SCROLLGROUP)


async def on_file(
    message: types.Message,
    widget: MessageInput,
    manager: DialogManager,
    item_id: str,
) -> None:
    await manager.done()

    await manager.start(Files.SCROLLGROUP, data={"file_id": item_id})
