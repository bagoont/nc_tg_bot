import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from bot.core import settings


def sg_languages(on_click) -> ScrollingGroup:
    return ScrollingGroup(
        Select(
            Format("{item[1]} {item[2]}"),
            id="files_select",
            item_id_getter=operator.itemgetter(0),
            items="languages",
            on_click=on_click,
        ),
        id="settings_lang_sg",
        width=3,
        height=settings.TG_SCROLLING_HEIGHT,
        hide_on_single_page=True,
    )
