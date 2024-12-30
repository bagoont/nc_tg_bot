from aiogram import types
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from bot.dialogs.files import keyboards
from bot.dialogs.search import getters, handlers
from bot.states import Search


def input_window() -> Window:
    return Window(
        Const("Write folder name."),
        MessageInput(
            handlers.search_query_handler,
            content_types=[types.ContentType.TEXT],
        ),
        Cancel(Const("Cancel")),
        state=Search.INPUT_QUERY,
    )


def scrollgroup_window() -> Window:
    return Window(
        Const("Search result"),
        keyboards.sg_fsnodes(handlers.on_file, items_key="fsnodes"),
        state=Search.SCROLLGROUP,
        getter=getters.get_fsnodes,
    )


def not_found_window() -> Window:
    return Window(
        Const("Not found."),
        state=Search.NOT_FOUND,
    )
