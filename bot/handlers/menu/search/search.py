"""Search handlers."""

from typing import cast

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud

from bot.handlers.core import get_search_msg
from bot.nextcloud import SearchService
from bot.states import SearchStatesGroup


async def start_search(message: Message, state: FSMContext, i18n: I18nContext) -> Message:
    """Initiate search process and ask user for the search text.

    Search entry point.

    :param message: Message object.
    :param state: State machine context.
    :param i18n: Internationalization context.
    """
    await state.set_state(SearchStatesGroup.SEARCH)

    return await message.reply(text=i18n.get("search-enter"))


async def search(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    nc: AsyncNextcloud,
) -> Message:
    """Search for files in the Nextcloud instance based on the given search text.

    :param message: Message object.
    :param state: State machine context.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    """
    msg_text = cast(str, message.text)

    await state.clear()

    srv = await SearchService.create_instance(nc, ["like", "name", f"%{message.text}%"])

    text, reply_markup = get_search_msg(i18n, msg_text, srv.fsnodes)
    return await message.reply(text=text, reply_markup=reply_markup)
