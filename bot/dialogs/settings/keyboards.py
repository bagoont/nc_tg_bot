import operator
from collections.abc import Callable

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from bot.core import settings


def sg_languages(on_click: Callable, *, items_key: str) -> ScrollingGroup:
    return ScrollingGroup(
        Select(
            Format("{item.language}"),
            id="lang_select",
            item_id_getter=operator.attrgetter("iso"),
            items=items_key,
            on_click=on_click,
        ),
        id="langs_sg",
        width=3,
        height=settings.TG_SCROLLING_HEIGHT,
        hide_on_single_page=True,
    )
