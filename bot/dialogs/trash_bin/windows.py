from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Const

from bot.dialogs.files import keyboards
from bot.dialogs.trash_bin import getters, handlers
from bot.states import Trash_bin


def scrollgroup_window() -> Window:
    return Window(
        Const("Trashbin"),
        keyboards.sg_fsnodes(handlers.on_trash, items_key="fsnodes"),
        state=Trash_bin.SCROLLGROUP,
        getter=getters.get_trash_bin,
    )


def trash_window() -> Window:
    return Window(
        Const("Trash"),
        Button(
            Const("Delete"),
            id="delete",
            on_click=handlers.on_delete,
        ),
        Button(
            Const("Restore"),
            id="restore",
            on_click=handlers.on_restore,
        ),
        SwitchTo(
            Const("Return"),
            id="back",
            state=Trash_bin.SCROLLGROUP,
        ),
        state=Trash_bin.TRASH,
    )


def multidelete_window() -> Window:
    return Window(
        Const("Select to delete."),
        keyboards.ms_sg_fsnodes(items_key="fsnodes"),
        Button(
            Const("Delete selected"),
            id="confirm",
            on_click=handlers.on_multidelete_confirm,
            when=F["dialog_data"]["checked_ids"],
        ),
        SwitchTo(
            Const("Back"),
            id="back",
            state=Trash_bin.SCROLLGROUP,
        ),
        state=Trash_bin.MULTISELECT,
    )


def cleanup_window() -> Window:
    return Window(
        Const("Cleanup"),
        Button(
            Const("Yes"),
            id="confirm",
            on_click=handlers.on_cleanup,
        ),
        SwitchTo(
            Const("No"),
            state=Trash_bin.SCROLLGROUP,
            id="back",
        ),
        state=Trash_bin.CLEANUP,
    )
