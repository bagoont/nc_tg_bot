from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from bot.handlers.settings import getters, handlers, keyboards
from bot.states import Settings


def main_window():
    return Window(
        Const("Settings."),
        Row(
            SwitchTo(
                Const("🚪 Logout"),
                id="settings_logout",
                state=Settings.LOGOUT,
            ),
            SwitchTo(
                Const("🌍 Language"),
                id="settings_lang",
                state=Settings.LANG,
            ),
        ),
        Cancel(
            Const("Exit"),
            id="settings_cancel",
        ),
        state=Settings.MAIN,
    )


def lang_window():
    return Window(
        Const("Language?"),
        keyboards.sg_languages(handlers.on_lang),
        state=Settings.LANG,
        getter=getters.get_languages,
    )


def logout_window():
    return Window(
        Const("Logout?"),
        Button(
            Const("Yes"),
            id="settings_logout_yes",
            on_click=handlers.on_logout,
        ),
        SwitchTo(
            Const("No"),
            id="settings_logout_no",
            state=Settings.MAIN,
        ),
        state=Settings.LOGOUT,
    )
