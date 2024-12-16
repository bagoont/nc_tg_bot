from aiogram import types
from aiogram_dialog import DialogManager
from nc_py_api import AsyncNextcloud, FsNode, NextcloudException

from bot.states import Search


async def _notify(event: types.TelegramObject, text: str, *, show_alert: bool = False) -> None:
    match event:
        case types.Message():
            await event.reply(text)
        case types.CallbackQuery():
            await event.answer(text, show_alert=show_alert)
        case _:
            # TODO: Write error message.
            raise TypeError


async def search_fsnodes(
    manager: DialogManager,
    nc: AsyncNextcloud,
    query: list[str],
    path: str | FsNode = "",
) -> None:
    try:
        fsnodes = await nc.files.find(query, path)
    except NextcloudException as e:
        await _notify(manager.event, e.reason, show_alert=True)
        await manager.done()
        return

    ctx = manager.current_context()
    ctx.dialog_data.update(fsnodes=fsnodes)

    if not fsnodes:
        await manager.switch_to(Search.NOT_FOUND)
        return
