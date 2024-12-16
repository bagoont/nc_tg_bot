from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from nc_py_api import AsyncNextcloud

from bot.db import UserRepository
from bot.states import Settings


async def on_lang(callback: types.CallbackQuery, widget: Select, manager: DialogManager, item_id: str) -> None:
    users: UserRepository = manager.middleware_data.get("users")

    user = await users.get_by_tg_id(manager.event.from_user.id)
    if user is None:
        # TODO: Send error message.
        return

    await users.update(user, language=item_id)
    await users.session.commit()

    await callback.answer(text=f'Language set to "{item_id}".')
    await manager.switch_to(Settings.MAIN)


async def on_logout(callback: types.CallbackQuery, widget: Button, manager: DialogManager) -> None:
    nc: AsyncNextcloud = manager.middleware_data.get("nc")
    users: UserRepository = manager.middleware_data.get("users")

    user = await users.get_by_tg_id(manager.event.from_user.id)
    if user is None:
        # TODO: Send error message.
        return

    await users.delete(user)
    await nc.ocs("DELETE", "/ocs/v2.php/core/apppassword")
    await users.session.commit()

    await callback.answer(text="Logout complete.")

    await manager.done()
