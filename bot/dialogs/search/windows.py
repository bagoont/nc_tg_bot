from aiogram import types
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Jinja

from bot.dialogs.files import keyboards
from bot.dialogs.search import getters, handlers
from bot.dialogs.search.states import Search


def input_query() -> Window:
    return Window(
        Jinja("{% for fsnode in fsnodes %}" "{{ fsnode.name }}"),
        MessageInput(
            handlers.search_query_handler,
            content_types=[types.ContentType.TEXT],
        ),
        Cancel(Const("__exit__")),
        state=Search.INPUT_QUERY,
    )


def scrollgroup() -> Window:
    return Window(
        Const("__search_result__"),
        keyboards.sg_fsnodes(handlers.on_file, items_key="fsnodes"),
        state=Search.SCROLLGROUP,
        getter=getters.get_fsnodes,
    )


def not_found() -> Window:
    return Window(
        Const("__not_found__"),
        state=Search.NOT_FOUND,
    )
