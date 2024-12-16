import operator

from aiogram_dialog.widgets.kbd import Multiselect, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from bot.core import settings


def sg_files(on_click) -> ScrollingGroup:
    return ScrollingGroup(
        Select(
            Format("{item[1]} {item[2]}"),
            id="files_select",
            item_id_getter=operator.itemgetter(0),
            items="fsnode_content",
            on_click=on_click,
        ),
        id="files_sg",
        width=1,
        height=settings.TG_SCROLLING_HEIGHT,
    )


def ms_sg_files(on_state_changed) -> ScrollingGroup:
    return ScrollingGroup(
        Multiselect(
            Format("✅ {item[1]} {item[2]}"),
            Format("☑️ {item[1]} {item[2]}"),
            id="files_ms",
            item_id_getter=operator.itemgetter(0),
            items="fsnode_content",
            on_state_changed=on_state_changed,
        ),
        id="files_ms_sg",
        width=1,
        height=settings.TG_SCROLLING_HEIGHT,
    )
