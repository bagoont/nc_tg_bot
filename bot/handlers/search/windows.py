from aiogram import types
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from bot.handlers.search import getters, handlers, keybaords
from bot.states import Search


def input_query_window() -> Window:
    return Window(
        Const("Write folder name."),
        MessageInput(
            handlers.search_query_handler,
            content_types=[types.ContentType.TEXT],
        ),
        Cancel(
            Const("Cancel"),
            id="search_cancel",
        ),
        state=Search.INPUT_QUERY,
    )


def search_result_window() -> Window:
    return Window(
        Const("Search result"),
        keybaords.sg_search_result(handlers.on_file),
        state=Search.SCROLLGROUP,
        getter=getters.get_fsnodes,
    )


def not_found_window() -> Window:
    return Window(
        Const("Not found."),
        state=Search.NOT_FOUND,
    )
