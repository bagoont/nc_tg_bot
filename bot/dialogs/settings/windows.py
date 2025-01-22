from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from bot.dialogs.settings import getters, handlers, keyboards
from bot.dialogs.settings.states import Settings


def main_window() -> Window:
    return Window(
        Const("Settings."),
        Row(
            SwitchTo(
                Const("🚪 Logout"),
                id="logout",
                state=Settings.LOGOUT,
            ),
            SwitchTo(
                Const("🌍 Language"),
                id="lang",
                state=Settings.LANG,
            ),
        ),
        Cancel(Const("Exit")),
        state=Settings.MAIN,
    )


def lang_window() -> Window:
    return Window(
        Const("Language?"),
        keyboards.sg_languages(handlers.on_lang, items_key="langs"),
        state=Settings.LANG,
        getter=getters.get_languages,
    )


def logout_window() -> Window:
    return Window(
        Const("Logout?"),
        Button(
            Const("Yes"),
            id="confirm",
            on_click=handlers.on_logout,
        ),
        SwitchTo(
            Const("No"),
            id="back",
            state=Settings.MAIN,
        ),
        state=Settings.LOGOUT,
    )
