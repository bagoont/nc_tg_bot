from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Const

from bot.dialogs.files import keyboards
from bot.dialogs.trashbin import getters, handlers
from bot.dialogs.trashbin.states import Trashbin


def scrollgroup() -> Window:
    return Window(
        Const("__trashbin__"),
        keyboards.sg_fsnodes(handlers.on_trash, items_key="fsnodes"),
        state=Trashbin.SCROLLGROUP,
        getter=getters.get_fsnodes,
    )


def trash_item() -> Window:
    return Window(
        Const("__trash_item__"),
        Button(
            Const("__delete__"),
            id="delete",
            on_click=handlers.on_delete,
        ),
        Button(
            Const("__restore__"),
            id="restore",
            on_click=handlers.on_restore,
        ),
        SwitchTo(
            Const("__back__"),
            id="back",
            state=Trashbin.SCROLLGROUP,
        ),
        state=Trashbin.TRASH,
    )


def cleanup() -> Window:
    return Window(
        Const("__cleanup__"),
        Button(
            Const("__yes__"),
            id="confirm",
            on_click=handlers.on_cleanup,
        ),
        SwitchTo(
            Const("__no__"),
            state=Trashbin.SCROLLGROUP,
            id="back",
        ),
        state=Trashbin.CLEANUP,
    )


def empty() -> Window:
    return Window(
        Const("__empty__"),
        state=Trashbin.EMPTY,
    )
